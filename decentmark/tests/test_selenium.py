from django.contrib.auth import get_user_model
from django.test import TestCase, LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from decentmark.models import *
from selenium.common import exceptions

class InitSelenium(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.browser = webdriver.Chrome()
        super(InitSelenium,cls).setUpClass()



    @classmethod
    def tearDownClass(cls):
        super(InitSelenium,cls).tearDownClass()
        cls.browser.quit()

    def perform_login(self,user_name,pass_word):     
        self.browser.get(self.live_server_url + '/accounts/login/')

        username = self.browser.find_element_by_name("username")
        username.send_keys(user_name)

        password = self.browser.find_element_by_name("password")
        password.send_keys(pass_word)

        self.browser.find_element_by_css_selector(".btn-primary").click()

    def perform_logout(self):
        self.browser.find_element_by_css_selector(".glyphicon-log-out").click()

    def perform_manual_mark(self,mark,feedback):
        manual_mark = self.browser.find_element_by_name("mark")
        manual_mark.clear()
        manual_mark.send_keys(mark)

        manual_feedback = self.browser.find_element_by_name("feedback")
        manual_feedback.clear()
        manual_feedback.send_keys(feedback)
        self.browser.find_element_by_css_selector(".btn-success").click()


class StudentsTests(InitSelenium):
    def setUp(self):
        User = get_user_model()
        self.student1=User.objects.create_user(username='stu',
                                 email='student1@decent.mark',
                                 password='stu')
        self.unit1=Unit.objects.create(name='Python', start='2017-10-25 14:30:59', end='2018-10-25 14:30:59', description='111',
                            deleted='False')
        UnitUsers.objects.create(unit=self.unit1, user=self.student1,create=False,mark=False,submit=True)
        self.assigngment1=Assignment.objects.create(unit=self.unit1,name='assigngment1',start='2018-10-24 14:30:59',end='2018-10-26 14:30:59',description='assignment1_discription',attempts=1,total=5, test='1',solution='1',template='1',deleted=False)
        self.unit2=Unit.objects.create(name='Django', start='2018-10-25 14:30:59', end='2017-10-25 14:30:59', description='222',
                            deleted='False')

    def tearDown(self):
        pass

    def perform_submission(self,example):           #submit a assignment function
        self.perform_login('stu','stu')
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/a").click()
        self.browser.find_element_by_css_selector(".btn-primary").click()
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/table/tbody/tr/td[1]/a").click()
        self.browser.find_element_by_css_selector(".btn-default").click()
        solution = self.browser.find_element_by_name("solution")
        solution.send_keys(example)
        self.browser.find_element_by_css_selector(".btn-success").click()

    def test_student_login_redirects_to_unit_list(self):     # student login test & view unit function
        self.perform_login('stu','stu')
        self.assertEqual(self.live_server_url + "/", self.browser.current_url, "At the Unit List page")

    def test_student_login_fail(self):     # student login fail test
        self.perform_login('stu','stu1')
        self.assertEqual(self.live_server_url + '/accounts/login/', self.browser.current_url, "At the Unit List page")

    def test_student_login_out_redirects_to_logout_page(self):     # student login out test
        self.perform_login('stu','stu')
        self.browser.find_element_by_xpath("/html/body/main/div[1]/div/a").click()
        self.assertEqual(self.live_server_url + '/accounts/logout/', self.browser.current_url)

    def test_student_login_out_redirects_to_login_page(self):     # student login out to login test
        self.perform_login('stu','stu')
        self.browser.find_element_by_xpath("/html/body/main/div[1]/div/a").click()
        self.browser.find_element_by_css_selector(".btn-primary").click()
        self.assertEqual(self.live_server_url + '/accounts/login/', self.browser.current_url)

    def test_student_navigation_home(self):     # student navigation to home test
        self.perform_login('stu','stu')
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/a").click()
        self.browser.find_element_by_xpath("/html/body/main/div[1]/ol/li/a").click()
        self.assertEqual(self.live_server_url + '/', self.browser.current_url)

    def test_student_redirects_to_create_assignment(self):  #permission check with manual navigation
        self.perform_login('stu','stu')
        self.browser.get(self.live_server_url + '/u/%d/create_assignment/' % self.unit1.id) #
        page_heading_text = self.browser.find_element_by_css_selector('h1').text
        self.assertEqual(page_heading_text, '403 Forbidden') #TO Do response code
      #  self.assertNotEqual(response.status_code, 200) #TO Do response code

    def test_student_not_enrolled_units_check(self):  #check wether units that the student is not enrolled in is displayed
        self.perform_login('stu','stu')
        def find_not_enrolled_unit():
            self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[1]/table/tbody/tr[2]/td[1]/a").click()
        self.assertRaises(exceptions.NoSuchElementException,find_not_enrolled_unit)


    def test_student_create_unit_button_check(self):  #check create unit button 
        self.perform_login('stu','stu')
        def find_create_unit():
            self.browser.find_element_by_css_selector('.btn-success')
        self.assertRaises(exceptions.NoSuchElementException,find_create_unit)

    def test_student_edit_unit_button_check(self):  #check edit unit button
        self.perform_login('stu','stu')
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/a").click()
        def find_edit_unit():
            self.browser.find_element_by_css_selector('.btn-danger')
        self.assertRaises(exceptions.NoSuchElementException,find_edit_unit)

    def test_student_invite_user_button_check(self):  #invite user buttion check 
        self.perform_login('stu','stu')
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/a").click()
        def find_invite_user():
            self.browser.find_element_by_css_selector('.btn-warning')
        self.assertRaises(exceptions.NoSuchElementException,find_invite_user)

    def test_student_audit_log_button_check(self):  #view audit log button check 
        self.perform_login('stu','stu')
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/a").click()
        def find_audit_log():
            self.browser.find_element_by_css_selector('.btn-secondary')
        self.assertRaises(exceptions.NoSuchElementException,find_audit_log)

    def test_student_view_a_unit(self):     # student login test & view unit function
        self.perform_login('stu','stu')
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/a").click()
        self.assertEqual(self.live_server_url + '/u/%d/' % self.unit1.id, self.browser.current_url,"At View a Unit Page")

    def test_student_unit_name_test(self):     # unit name is well displayed
        self.perform_login('stu','stu')
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/a").click()
        unit_name=self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[1]/p").text
        self.assertEqual(unit_name, self.unit1.name,"At View a Unit Page")

    def test_student_view_assignments(self):     # student view assignment list function
        self.perform_login('stu','stu')
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/a").click()
        self.browser.find_element_by_css_selector(".btn-primary").click()
        self.assertEqual(self.live_server_url + '/u/%d/assignments/' % self.unit1.id, self.browser.current_url,"At assignment Lists Page")

    def test_student_create_a_assignment(self):     # create a assignment button check
        self.perform_login('stu','stu')
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/a").click()
        self.browser.find_element_by_css_selector(".btn-primary").click()
        def find_create_assignment():
            self.browser.find_element_by_css_selector('.btn-primary')
        self.assertRaises(exceptions.NoSuchElementException,find_create_assignment)

    def test_student_view_a_assignment(self):     # student view a ssignment function
        self.perform_login('stu','stu')
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/a").click()
        self.browser.find_element_by_css_selector(".btn-primary").click()
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/table/tbody/tr/td[1]/a").click()
        self.assertEqual(self.live_server_url + '/a/%d/' % self.assigngment1.id,self.browser.current_url,"At View a assignment Page")

    def test_student_edit_a_assignment(self):     # student edit assignment function permission
        self.perform_login('stu','stu')
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/a").click()
        self.browser.find_element_by_css_selector(".btn-primary").click()
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/table/tbody/tr/td[1]/a").click()
        def find_edit_assignment():
            self.browser.find_element_by_css_selector('.btn-danger')
        self.assertRaises(exceptions.NoSuchElementException,find_edit_assignment)

    def test_student_view_a_assignment_name(self):     # student view a ssignment function
        self.perform_login('stu','stu')
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/a").click()
        self.browser.find_element_by_css_selector(".btn-primary").click()
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/table/tbody/tr/td[1]/a").click()
        assignment_name=self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[1]/p").text
        self.assertEqual(assignment_name,self.assigngment1.name)

    def test_student_make_a_submission(self):                   #student make a submission
        self.perform_submission("sample_solution")
        solution_area=self.browser.find_element_by_xpath("/html/body/main/div[2]/div/table/tbody/tr[3]/td").text
        self.assertEqual(solution_area,"sample_solution")

    def test_student_mark_a_submission(self):                   #student mark a submission
        self.perform_submission("sample_solution")
        def find_mark_assignment():
            self.browser.find_element_by_css_selector('.btn-warning')
        self.assertRaises(exceptions.NoSuchElementException,find_mark_assignment)

    def test_student_viwe_a_submission(self):                   #student view a submission
        self.perform_submission("sample_solution1")
        self.browser.find_element_by_css_selector(".btn-info").click()
        submission_area=self.browser.find_element_by_xpath("/html/body/main/div[2]/table/tbody/tr[1]/td[1]").text
        self.assertEqual(submission_area,self.student1.username)


        #self.assertEqual(self.live_server_url + "/u/4/", self.browser.current_url, "At the Unit List page")

    def test_student_edit_profile(self):
        pass

    def test_student_download_submission(self):
        pass
    # TO DO:
        # respond code & self.assertEqual(response.status_code, 403)
        # check content & url

class TeachersTests(InitSelenium):
    def setUp(self):
        User = get_user_model()
        self.student1=User.objects.create_user(username='stu',
                                 email='student1@decent.mark',
                                 password='stu')
        self.teacher1=User.objects.create_user(username='teacher',
                                 email='student1@decent.mark',
                                 password='teacher')
        self.unit1=Unit.objects.create(name='Python', start='2018-10-25 14:30:59', end='2018-11-25 14:30:59', description='111')
        UnitUsers.objects.create(unit=self.unit1, user=self.teacher1,create=True,mark=True,submit=False)
        UnitUsers.objects.create(unit=self.unit1, user=self.student1,create=False,mark=False,submit=True)


        self.assignment1=Assignment.objects.create(unit=self.unit1,name='assigngment1',start='2018-10-24 14:30:59',end='2018-10-26 14:30:59',description='assignment1_discription',attempts=1,total=5, test='1',solution='1',template='1',deleted=False)
        self.submission1=Submission.objects.create(assignment=self.assignment1,user=self.student1,solution="sample_solution")


    def tearDown(self):
        pass


    def test_teacher_login_fail(self):     # teacher login with wrong answer
        self.perform_login('teacher1','teacher')
        self.assertEqual(self.live_server_url + '/accounts/login/', self.browser.current_url, "At the Unit List page")

    def test_teacher_login_redirects_to_unit_list(self):     # teacher login test & view unit function
        self.perform_login('teacher','teacher')
        self.assertEqual(self.live_server_url + "/", self.browser.current_url, "At the Unit List page")


    def test_teacher_login_out_redirects_to_logout_page(self):     # teacher login out test
        self.perform_login('teacher','teacher')
        self.browser.find_element_by_xpath("/html/body/main/div[1]/div/a").click()
        self.assertEqual(self.live_server_url + '/accounts/logout/', self.browser.current_url)

    def test_teacher_login_out_redirects_to_login_page(self):     # teacher login out to login test
        self.perform_login('teacher','teacher')
        self.browser.find_element_by_xpath("/html/body/main/div[1]/div/a").click()
        self.browser.find_element_by_css_selector(".btn-primary").click()
        self.assertEqual(self.live_server_url + '/accounts/login/', self.browser.current_url)


    def test_teacher_view_a_unit(self):     # teacher view a unit
        self.perform_login('teacher','teacher')
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/a").click()
        page_heading_text = self.browser.find_element_by_css_selector('h4').text
        self.assertEqual(page_heading_text, "Unit Name", "At Unit Page")

    def test_teacher_view_assignments(self):     # teacher view assignments
        self.perform_login('teacher','teacher')
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/a").click()
        self.browser.find_element_by_css_selector(".btn-primary").click()
        page_heading_text = self.browser.find_element_by_xpath('/html/body/main/div/div/h1').text
        self.assertEqual(page_heading_text,"Python Assignments", "At assignments Page")

    def test_teacher_view_a_assignment(self):     # teacher view a assignment
        self.perform_login('teacher','teacher')
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/a").click()
        self.browser.find_element_by_css_selector(".btn-primary").click()
        self.browser.find_element_by_xpath("/html/body/main/div/div/table/tbody/tr/td[1]/a").click()
        page_heading_text = self.browser.find_element_by_xpath('/html/body/main/div/div/div[1]/p').text
        self.assertEqual(page_heading_text,"assigngment1", "At assignment Page")

    def test_teacher_make_a_submission(self):                   #teacher make a submission button check, permission check
        self.perform_login('teacher','teacher')
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/a").click()
        self.browser.find_element_by_css_selector(".btn-primary").click()
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/table/tbody/tr/td[1]/a").click()
        def find_make_a_submission_teacher():
            self.browser.find_element_by_css_selector('.btn-default')
        self.assertRaises(exceptions.NoSuchElementException,find_make_a_submission_teacher)

    def test_teacher_view_all_submissions(self):                   #teacher view all submissions
        self.perform_login('teacher','teacher')
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/a").click()
        self.browser.find_element_by_css_selector(".btn-primary").click()
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/table/tbody/tr/td[1]/a").click()
        self.browser.find_element_by_css_selector(".btn-primary").click()
        submission_name=self.browser.find_element_by_xpath("/html/body/main/div[2]/table/tbody/tr[1]/td[1]/a").text
        self.assertEqual(submission_name,"stu")


    def test_teacher_view_a_submission(self):                   #teacher view a submission
        self.perform_login('teacher','teacher')
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/a").click()
        self.browser.find_element_by_css_selector(".btn-primary").click()
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/table/tbody/tr/td[1]/a").click()
        self.browser.find_element_by_css_selector(".btn-primary").click()
        self.browser.find_element_by_xpath("/html/body/main/div[2]/table/tbody/tr[1]/td[1]/a").click()
        header=self.browser.find_element_by_xpath("/html/body/main/div[2]/div/h1").text
        self.assertEqual(header,self.assignment1.name+" by "+self.submission1.user.username)

    def test_teacher_manual_feedback(self):
        self.perform_login('teacher','teacher')
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/a").click()
        self.browser.find_element_by_css_selector(".btn-primary").click()
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/table/tbody/tr/td[1]/a").click()
        self.browser.find_element_by_css_selector(".btn-primary").click()
        self.browser.find_element_by_xpath("/html/body/main/div[2]/table/tbody/tr[1]/td[1]/a").click()
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/h1").click()
        self.browser.find_element_by_css_selector(".btn-warning").click()
        mark=4
        feedback="HD"
        self.perform_manual_mark(mark,feedback)
        feedback_area=self.browser.find_element_by_xpath("/html/body/main/div[2]/div/table/tbody/tr[7]/td").text
        self.assertEqual(feedback_area,feedback)

    def test_teacher_manual_score(self):
        self.perform_login('teacher','teacher')
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/a").click()
        self.browser.find_element_by_css_selector(".btn-primary").click()
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/table/tbody/tr/td[1]/a").click()
        self.browser.find_element_by_css_selector(".btn-primary").click()
        self.browser.find_element_by_xpath("/html/body/main/div[2]/table/tbody/tr[1]/td[1]/a").click()
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/h1").click()
        self.browser.find_element_by_css_selector(".btn-warning").click()
        mark=4
        feedback="HD"
        self.perform_manual_mark(mark,feedback)
        score_area=self.browser.find_element_by_xpath("/html/body/main/div[2]/div/table/tbody/tr[6]/td").text
        self.assertEqual(score_area,"%d / %d" % (mark,self.assignment1.total))

    def perform_edit_unit(self,name,start,end,discription):
        ele_name = self.browser.find_element_by_name("name")
        ele_name.clear()
        ele_name.send_keys(name)

        ele_start = self.browser.find_element_by_name("start")
        ele_start.click()
        ele_start.send_keys(start)

        ele_end = self.browser.find_element_by_name("end")
        ele_end.click()
        ele_end.send_keys(end)

        ele_discription = self.browser.find_element_by_name("description")
        ele_discription.clear()
        ele_discription.send_keys(discription)

        self.browser.find_element_by_css_selector(".btn-primary").click()

    def test_teacher_edit_unit(self):
        self.perform_login('teacher','teacher')
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/a").click()
        self.browser.find_element_by_css_selector(".btn-danger").click()
        unitname="unit2"
        startdate="01062018"
        enddate="09062018"
        discription="unit2_discription"
        self.perform_edit_unit(unitname,startdate,enddate,discription)
        unit_name=self.browser.find_element_by_css_selector(".well-sm").text
        self.assertEqual(unit_name,unitname)

    def perform_create_assignment(self,name,start,end,discription,total,test,solution,template):
        
        ele_name = self.browser.find_element_by_name("name")
        ele_name.clear()
        ele_name.send_keys(name)

        ele_start = self.browser.find_element_by_name("start")
        ele_start.click()
        ele_start.send_keys(start)

        ele_end = self.browser.find_element_by_name("end")
        ele_end.click()
        ele_end.send_keys(end)

        ele_discription = self.browser.find_element_by_name("description")
        ele_discription.clear()
        ele_discription.send_keys(discription)

        ele_total = self.browser.find_element_by_name("total")
        ele_total.clear()
        ele_total.send_keys(total)

        ele_total = self.browser.find_element_by_name("test")
        ele_total.clear()
        ele_total.send_keys(test)

        ele_total = self.browser.find_element_by_name("solution")
        ele_total.clear()
        ele_total.send_keys(solution)

        ele_total = self.browser.find_element_by_name("template")
        ele_total.clear()
        ele_total.send_keys(template)

        self.browser.find_element_by_css_selector(".btn-primary").click()

    def test_teacher_create_assignment(self):
        self.perform_login('teacher','teacher')
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/a").click()
        self.browser.find_element_by_css_selector(".btn-primary").click()
        self.browser.find_element_by_css_selector(".btn-primary").click()
        name="assignemnt2"
        start="03072019"
        end="19072019"
        discription="assignemnt2_discription"
        total=10
        test="assignment2_test"
        solution="assignment2_solution"
        template="assignment2_template"
        self.perform_create_assignment(name,start,end,discription,total,test,solution,template)
        assignment_name=self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[1]/p").text
        self.assertEqual(assignment_name,name)

    def perform_edit_assignment(self,name,start,end,discription,total,test,solution,template):
        

        ele_discription = self.browser.find_element_by_name("description")
        ele_discription.clear()
        ele_discription.send_keys(discription)


        self.browser.find_element_by_css_selector(".btn-primary").click()

    def test_teacher_edit_assignment(self):
        self.perform_login('teacher','teacher')
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/a").click()
        self.browser.find_element_by_css_selector(".btn-primary").click()
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/table/tbody/tr[1]/td[1]/a").click()
        self.browser.find_element_by_css_selector(".btn-danger").click()
        name="assignemnt2"
        start="03072019"
        end="19072019"
        discription="assignemnt2_discription_new"
        total=10
        test="assignment2_test"
        solution="assignment2_solution"
        template="assignment2_template"
        self.perform_edit_assignment(name,start,end,discription,total,test,solution,template)
        discription_name=self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[2]/p").text
        self.assertEqual(discription_name,discription)


    def test_teacher_create_unit(self):
        pass
    def test_teacher_auto_score_and_feedback(self):
        pass

    def test_teacher_invite_users(self):
        pass

    def test_teacher_view_users(self):
        pass
    def test_teacher_download_all_submissions(self):
        pass
    def test_teacher_download_a_submission(self):
        pass
    def test_teacher_edit_profile(self):
        pass

    def test_teacher_edit_audit_log(self):
        pass




class MarkersTests(InitSelenium):
    def setUp(self):
        User = get_user_model()
        self.student1=User.objects.create_user(username='stu',
                                 email='student1@decent.mark',
                                 password='stu')
        self.marker1=User.objects.create_user(username='marker',
                                 email='student1@decent.mark',
                                 password='marker')
        self.unit1=Unit.objects.create(name='Python', start='2018-10-25 14:30:59', end='2018-11-25 14:30:59', description='111',
                            deleted=False)
        UnitUsers.objects.create(unit=self.unit1, user=self.marker1,create=False,mark=True,submit=False)
        UnitUsers.objects.create(unit=self.unit1, user=self.student1,create=False,mark=False,submit=True)

        self.assignment1=Assignment.objects.create(id=2,unit=self.unit1,name='assigngment1',start='2018-10-24 14:30:59',end='2018-10-26 14:30:59',description='assignment1_discription',attempts=1,total=5, test='1',solution='1',template='1',deleted=False)
        self.submission1=Submission.objects.create(assignment=self.assignment1,user=self.student1,solution="sample_solution")


    def tearDown(self):
        pass


    def test_marker_login_fail(self):     # marker login with wrong answer
        self.perform_login('marker1','marker')
        self.assertEqual(self.live_server_url + '/accounts/login/', self.browser.current_url, "At the Unit List page")

    def test_marker_login_redirects_to_unit_list(self):     # marker login test & view unit function
        self.perform_login('marker','marker')
        self.assertEqual(self.live_server_url + "/", self.browser.current_url, "At the Unit List page")

    def test_marker_login_out_redirects_to_logout_page(self):     # marker login out test
        self.perform_login('marker','marker')
        self.browser.find_element_by_xpath("/html/body/main/div[1]/div/a").click()
        self.assertEqual(self.live_server_url + '/accounts/logout/', self.browser.current_url)

    def test_marker_login_out_redirects_to_login_page(self):     # marker login out to login test
        self.perform_login('marker','marker')
        self.browser.find_element_by_xpath("/html/body/main/div[1]/div/a").click()
        self.browser.find_element_by_css_selector(".btn-primary").click()
        self.assertEqual(self.live_server_url + '/accounts/login/', self.browser.current_url)


    def test_marker_view_a_unit(self):     # marker view a unit
        self.perform_login('marker','marker')
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/a").click()
        page_heading_text = self.browser.find_element_by_css_selector('h4').text
        self.assertEqual(page_heading_text, "Unit Name", "At Unit Page")

    def test_marker_view_assignments(self):     # marker view assignments
        self.perform_login('marker','marker')
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/a").click()
        self.browser.find_element_by_css_selector(".btn-primary").click()
        page_heading_text = self.browser.find_element_by_xpath('/html/body/main/div/div/h1').text
        self.assertEqual(page_heading_text,"Python Assignments", "At assignments Page")

    def test_marker_view_a_assignment(self):     # marker view a assignment
        self.perform_login('marker','marker')
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/a").click()
        self.browser.find_element_by_css_selector(".btn-primary").click()
        self.browser.find_element_by_xpath("/html/body/main/div/div/table/tbody/tr/td[1]/a").click()
        page_heading_text = self.browser.find_element_by_xpath('/html/body/main/div/div/div[1]/p').text
        self.assertEqual(page_heading_text,"assigngment1", "At assignment Page")

    def test_marker_make_a_submission(self):                   #marker make a submission button check, permission check
        self.perform_login('marker','marker')
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/a").click()
        self.browser.find_element_by_css_selector(".btn-primary").click()
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/table/tbody/tr/td[1]/a").click()
        def find_make_a_submission_marker():
            self.browser.find_element_by_css_selector('.btn-default')
        self.assertRaises(exceptions.NoSuchElementException,find_make_a_submission_marker)

    def test_marker_view_all_submissions(self):                   #marker view all submissions
        self.perform_login('marker','marker')
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/a").click()
        self.browser.find_element_by_css_selector(".btn-primary").click()
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/table/tbody/tr/td[1]/a").click()
        self.browser.find_element_by_css_selector(".btn-primary").click()
        submission_name=self.browser.find_element_by_xpath("/html/body/main/div[2]/table/tbody/tr[1]/td[1]/a").text
        self.assertEqual(submission_name,"stu")

    def test_marker_view_a_submission(self):                   #marker view a submission
        self.perform_login('marker','marker')
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/a").click()
        self.browser.find_element_by_css_selector(".btn-primary").click()
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/table/tbody/tr/td[1]/a").click()
        self.browser.find_element_by_css_selector(".btn-primary").click()
        self.browser.find_element_by_xpath("/html/body/main/div[2]/table/tbody/tr[1]/td[1]/a").click()
        header=self.browser.find_element_by_xpath("/html/body/main/div[2]/div/h1").text
        self.assertEqual(header,self.assignment1.name+" by "+self.submission1.user.username)

    def test_marker_manual_feedback(self):
        self.perform_login('marker','marker')
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/a").click()
        self.browser.find_element_by_css_selector(".btn-primary").click()
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/table/tbody/tr/td[1]/a").click()
        self.browser.find_element_by_css_selector(".btn-primary").click()
        self.browser.find_element_by_xpath("/html/body/main/div[2]/table/tbody/tr[1]/td[1]/a").click()
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/h1").click()
        self.browser.find_element_by_css_selector(".btn-warning").click()
        mark=3
        feedback="D"
        self.perform_manual_mark(mark,feedback)
        feedback_area=self.browser.find_element_by_xpath("/html/body/main/div[2]/div/table/tbody/tr[7]/td").text
        self.assertEqual(feedback_area,feedback)

    def test_marker_manual_score(self):
        self.perform_login('marker','marker')
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/a").click()
        self.browser.find_element_by_css_selector(".btn-primary").click()
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/table/tbody/tr/td[1]/a").click()
        self.browser.find_element_by_css_selector(".btn-primary").click()
        self.browser.find_element_by_xpath("/html/body/main/div[2]/table/tbody/tr[1]/td[1]/a").click()
        self.browser.find_element_by_xpath("/html/body/main/div[2]/div/h1").click()
        self.browser.find_element_by_css_selector(".btn-warning").click()
        mark=3
        feedback="D"
        self.perform_manual_mark(mark,feedback)
        score_area=self.browser.find_element_by_xpath("/html/body/main/div[2]/div/table/tbody/tr[6]/td").text
        self.assertEqual(score_area,"%d / %d" % (mark,self.assignment1.total))
    def test_marker_auto_score_and_feedback(self):
        pass
    def test_marker_download_all_submissions(self):
        pass
    def test_marker_download_a_submission(self):
        pass
    def test_marker_edit_profile(self):
        pass
    def test_marker_view_users(self):
        pass

    def test_marker_more_permission_check(self):
        pass








