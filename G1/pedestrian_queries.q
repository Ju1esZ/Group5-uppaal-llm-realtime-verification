// Q1: 全局无死锁
A[] not deadlock

// Q2: 行人穿越时必须显示行人绿灯
A[] (PedestrianProcess.Crossing imply signal == PED_GREEN)

// Q3: 行人占用路口时，控制器必须处于行人绿灯位置
A[] (pedestrianCrossing imply Controller.PedestrianGreen)

// Q4: 行人穿越与车辆绿灯不能同时出现
A[] not (PedestrianProcess.Crossing && Controller.CarGreen)

// Q5: 至少存在一条行人完成通行的路径
E<> PedestrianProcess.Done

// Q6: 每次等待最终都会完成通行（活性）
PedestrianProcess.Waiting --> PedestrianProcess.Done

// Q7: 行人等待不超过 13 秒（WAIT_BOUND 由 12 修正为 13：循环场景下请求可落在绿灯周期起点）
A[] (PedestrianProcess.Waiting imply waitClock <= WAIT_BOUND)

// Q8: 行人穿越不超过 4 秒
A[] (PedestrianProcess.Crossing imply PedestrianProcess.crossingClock <= CROSSING_MAX)
