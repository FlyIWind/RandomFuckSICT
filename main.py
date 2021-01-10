import json
import random
import time
import traceback
import sched
from yiban import YiBan
import util



def main(phone_number,password):
    try:
        yb = YiBan(phone_number, password)
        yb.login()
        yb.getHome()
        print("登录成功 %s"%yb.name)
        yb.auth()
        all_task = yb.getUncompletedList()["data"]
        print(all_task)
        all_task = list(filter(lambda x: "体温上报" in x["Title"], all_task))
        if len(all_task) == 0:
            print("没找到今天体温上报的任务，可能是你已经上报，如果不是请手动上报。")
        else:
            all_task_sort = util.desc_sort(all_task, "StartTime")
            new_task = all_task_sort[0]
            print("找到未上报的任务：", new_task)
            task_detail = yb.getTaskDetail(new_task["TaskId"])["data"]
            ex = {"TaskId": task_detail["Id"],
                "title": "任务信息",
                "content": [{"label": "任务名称", "value": task_detail["Title"]},
                            {"label": "发布机构", "value": task_detail["PubOrgName"]},
                            {"label": "发布人", "value": task_detail["PubPersonName"]}]}
            dict_form = {"361a5d69d6db93e55bb656b4185e0447": ["36.2", "36.3", "36.4", "36.5"][random.randint(0, 3)],
                        "8f9a18d14676aa05e2dc26637225ffa4": ["36.2", "36.3", "36.4", "36.5"][random.randint(0, 3)],
                        "966c57278836ba050a382a5b70de7582": ["36.2", "36.3", "36.4", "36.5"][random.randint(0, 3)]}
            submit_result = yb.submit(json.dumps(dict_form, ensure_ascii=False), json.dumps(
                ex, ensure_ascii=False), task_detail["WFId"])
            if submit_result["code"] == 0:
                share_url = yb.getShareUrl(submit_result["data"])["data"]["uri"]
                print("已完成一次体温上报[%s]" % task_detail["Title"])
                print("访问此网址查看详情：%s" % share_url)
            else:
                print("[%s]遇到了一些错误:%s" % (task_detail["Title"], submit_result["msg"]))
    except Exception as e:
        print("出错啦")
        print(e)




if __name__ == '__main__':
    inc = random.randint(0, 900)#TODO:修改第二个参数为你要延迟上报的随机时间最大值，单位秒
    schedule = sched.scheduler(time.time, time.sleep)
    print("%s后进行上报" % inc)
    schedule.enter(inc, 0, main, ("手机号", "密码"))#TODO:修改为你的手机号和密码
    schedule.run()
