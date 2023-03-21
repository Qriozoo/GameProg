def test_script(script, test):
    print(script)
    print(test)

    params = '5'
    answ_func = """%s \nansw = sol_func(%s)"""

    try:
        tests = test.split('\n')
        for test in tests:
            test_num = test.split(':')[0]
            in_data = test.split(',')[0].split('-')[1].strip(" ")
            out_data = int(test.split(',')[1].split('-')[1].strip(" "))

            loc = {}
            exec(answ_func % (script, in_data), globals(), loc)
            return_workaround = loc['answ']

            if return_workaround == out_data:
                print("%s - %s" % (test_num, "True"))
            else:
                print("%s - %s" % (test_num, "False"))


    except Exception as ex:
        print(ex)
    return