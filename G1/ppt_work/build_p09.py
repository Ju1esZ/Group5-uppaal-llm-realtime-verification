import sys

sys.path.insert(0, "/Users/lj/Library/Application Support/Doubao/Default/.doubao/agent_mode/workspace/.skills/ppt")

from scripts.gen_svg_charts import chart_slide
from scripts.svg_lib.atomize_svg_to_slide import publish_slide

DECK = "Pqn1syGYIlgmoJd1W6Qc3NQqnJf"

page_xml = """<slide xmlns="https://www.larkoffice.com/sml/2.0"><style><fill><fillColor color="rgb(252,252,250)"/></fill></style><data>
  <shape type="text" topLeftX="48" topLeftY="30" width="840" height="34"><content fontSize="24" fontFamily="思源宋体" bold="true" color="rgb(24,38,58)"><p>等待上界不是拍的：一次反例把 12 秒改成 13 秒</p></content></shape>
  <line startX="48" startY="80" endX="912" endY="80"><border color="rgb(203,212,222)" width="1"/></line>
  <shape type="text" topLeftX="48" topLeftY="88" width="860" height="20"><content fontSize="11" color="rgb(105,120,140)"><p>横轴：请求落在车辆绿灯周期内的第几秒；纵轴：该请求必须等多久（黄灯 2 秒 + 全红 1 秒为固定开销）</p></content></shape>
  <shape type="text" topLeftX="640" topLeftY="112" width="272" height="20"><content fontSize="11" color="rgb(81,157,120)" bold="true" letterSpacing="1"><p>结论怎么来的</p></content></shape>
  <line startX="640" startY="134" endX="640" endY="440"><border color="rgb(203,212,222)" width="1"/></line>
  <shape type="text" topLeftX="654" topLeftY="142" width="258" height="76"><content fontSize="11" color="rgb(24,38,58)" lineSpacing="multiple:1.45"><p>初版按“最短剩余绿灯”推：1 秒到达 → 12 秒。这个推导把最坏情形算成了最好情形。</p></content></shape>
  <shape type="text" topLeftX="654" topLeftY="226" width="258" height="90"><content fontSize="11" color="rgb(24,38,58)" lineSpacing="multiple:1.45"><p>UPPAAL 给出的反例里，请求落在绿灯周期的第 0 秒，剩余绿灯 10 秒，实际等待 10+2+1=13 秒，12 秒的断言被推翻。</p></content></shape>
  <shape type="text" topLeftX="654" topLeftY="324" width="258" height="90"><content fontSize="11" color="rgb(24,38,58)" lineSpacing="multiple:1.45"><p>把 WAIT_BOUND 改为 13 并同步改注释与查询后重跑，第 7 条才真正 satisfied。这是全项目唯一一次被反例改回来的参数。</p></content></shape>
  <line startX="48" startY="452" endX="912" endY="452"><border color="rgb(224,229,235)" width="1"/></line>
  <shape type="text" topLeftX="48" topLeftY="460" width="860" height="20"><content fontSize="10" color="rgb(105,120,140)"><p>图中折线由模型常量与反例时间戳推出，非模拟数据；初版 12 秒的水平参考线保留以示对照</p></content></shape>
</data></slide>"""

pts = [{"x": t, "y": 13 - t} for t in range(0, 11)]

frag = chart_slide(
    "scatter",
    40,
    108,
    576,
    330,
    points=[{"name": "必须等待时长 13 - t", "points": pts, "curve": pts, "marker": "circle", "fit": None}],
    x_title="请求落在绿灯第 t 秒（t = 0..10）",
    y_title="等待时长（秒）",
    y_unit="",
    show_ci=False,
    fit=None,
    reference_lines=[{"value": 12, "label": "初版上界 12 秒"}],
    end_labels=False,
    palette="sci_bluegreen",
    font_family="思源黑体",
)

r = publish_slide(page_xml, frag, presentation=DECK, page=9)
print(r["ok"], r.get("slide_id"))
print("\n".join(r.get("summary", [])))
