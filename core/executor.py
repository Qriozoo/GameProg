def test_script(script, test):
    result = []
    answ_func = """%s \nansw = foo(%s)"""

    try:
        tests = test.split('\n')
        for test in tests:
            test_num = test.split(':')[0]
            in_data = test.split(';')[0].split('-')[1].strip(" ")
            out_data = test.split(';')[1].split('-')[1].strip(" ")

            loc = {}
            exec(answ_func % (script, in_data), globals(), loc)
            return_workaround = loc['answ']
            
            out_loc = {}
            exec("res = %s" % (out_data), globals(), out_loc)
            out_res = out_loc['res']
            if return_workaround == out_res:
                result.append("%s - %s" % (test_num, "True"))
            else:
                result.append("%s - %s" % (test_num, "False"))
        return result

    except Exception as ex:
        return ex
    return