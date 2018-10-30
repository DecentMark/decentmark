CODE_TEMPLATES = {'python3': '''
import json
${HELPER_CODE}

${SOLUTION}

if __name__ == '__main__':
    print(json.dumps(${TEST_CASE}))
'''
                 }
