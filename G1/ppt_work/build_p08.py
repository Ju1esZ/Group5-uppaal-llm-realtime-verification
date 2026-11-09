import sys

sys.path.insert(0, "/Users/lj/Library/Application Support/Doubao/Default/.doubao/agent_mode/workspace/.skills/ppt")

from scripts.gen_svg_charts import chart_slide
from scripts.svg_lib.atomize_svg_to_slide import publish_slide

DECK = "Pqn1syGYIlgmoJd1W6Qc3NQqnJf"

page_xml = """<slide xmlns="https://www.larkoffice.com/sml/2.0"><style><fill><fillColor color="rgb(252,252,250)"/></fill></style><data>
  <shape type="text" topLeftX="48" topLeftY="30" width="840" height="34"><content fontSize="24" fontFamily="思源宋体" bold="true" color="rgb(24,38,58)"><p>一个请求周期 15 秒：灯序与等待是同一张表的两列</p></content></shape>
  <line startX="48" startY="80" endX="912" endY="80"><border color="rgb(203,212,222)" width="1"/></line>
  <shape type="text" topLeftX="48" topLeftY="88" width="860" height="20"><content fontSize="11" color="rgb(105,120,140)"><p>取最晚的一次请求：绿灯已走过 8 秒才提出请求，此时剩余通行时间最短，等待反而最长</p></content></shape>
  <shape type="text" topLeftX="48" topLeftY="452" width="264" height="46"><content fontSize="11" color="rgb(24,38,58)" lineSpacing="multiple:1.4"><p>黄灯 2 秒 + 全红 1 秒是固定开销，任何请求都要先付这 3 秒</p></content></shape>
  <shape type="text" topLeftX="330" topLeftY="452" width="264" height="46"><content fontSize="11" color="rgb(24,38,58)" lineSpacing="multiple:1.4"><p>行人绿灯窗口里要留 3–4 秒给穿越，少于 3 秒不满足 CROSSING_MIN</p></content></shape>
  <shape type="text" topLeftX="612" topLeftY="452" width="300" height="46"><content fontSize="11" color="rgb(24,38,58)" lineSpacing="multiple:1.4"><p>收尾再插一段全红，之后才允许车辆恢复绿灯，冲突窗口被彻底关闭</p></content></shape>
</data></slide>"""

frag = chart_slide(
    "gantt",
    40,
    106,
    880,
    336,
    tasks=[
        ["车辆绿灯（剩余）", 0, 2],
        ["车辆黄灯", 2, 4],
        ["全红清空", 4, 5],
        ["行人绿灯 + 穿越", 5, 9],
        ["全红收尾", 9, 10],
        ["车辆绿灯恢复", 10, 15],
    ],
    weeks=15,
    critical_index=3,
    milestones=[[0, "请求到达"], [10, "穿越完成"]],
    time_unit="s",
    show_kpi=False,
    show_legend=True,
    palette="sci_bluegreen",
    font_family="思源黑体",
)

r = publish_slide(page_xml, frag, presentation=DECK, page=8)
print(r["ok"], r.get("slide_id"))
print("\n".join(r.get("summary", [])))
