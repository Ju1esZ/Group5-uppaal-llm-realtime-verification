// G5 基础无死锁属性
A[] not deadlock

// 路口占用期间信号保持绿灯
A[] (VehicleProcess.Crossing imply signal == GREEN)

// 至少存在一条完成通行的执行路径
E<> VehicleProcess.Done
