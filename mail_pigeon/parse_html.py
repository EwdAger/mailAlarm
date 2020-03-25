# coding=utf-8
"""
Created on 2020/3/25 17:31

@author: EwdAger
"""


def format_html(now_date, members, body):
    template = f"""
        <table color="CCCC33" width="800" border="1" cellspacing="0" cellpadding="5" text-align="center">
            <thead>
                <tr>
                    <th>日期</th>
                    <td>{now_date}</td>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <th>与会人</th>
                    <td>{members}</td>
                </tr>
            </tbody>

            
        </table>
            <hr>
            <table color="CCCC33" width="800" border="1" cellspacing="0" cellpadding="5" text-align="center">
            <caption>今日工作任务完成情况及明日计划：</caption>
            <thead>
                <tr>
                    <th>姓名</th>
                    <th>行动描述</th>
                </tr>
            </thead>
            <tbody>
                
                {body}
            </tbody>
    </table>
    """
    return template


def format_body(daily_dict):
    table = ''
    for name, daily in daily_dict.items():
        body = f"""
                <tr>
                    <th>{name}</th>
                    <td>{daily}</td>
                </tr>
                \n
        """
        table += body
    return table
