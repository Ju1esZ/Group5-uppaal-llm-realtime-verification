```xml
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE nta PUBLIC '-//Uppaal Team//DTD Flat System 1.1//EN' 'http://www.it.uu.se/research/group/darts/uppaal/flat-1_2.dtd'>
<nta>
  <declaration>
// 时间单位：秒。
// 仅在绿灯的前 17 秒允许车辆开始通行，预留最多 3 秒清空路口。
urgent chan pass;
bool green = true;
  </declaration>

  <template>
    <name>TrafficLight</name>
    <declaration>clock t;</declaration>

    <location id="light_green" x="0" y="0">
      <name x="-25" y="-30">Green</name>
      <label kind="invariant" x="-25" y="20">t &lt;= 17</label>
    </location>
    <location id="light_clearance" x="240" y="0">
      <name x="190" y="-30">GreenClearance</name>
      <label kind="invariant" x="215" y="20">t &lt;= 20</label>
    </location>
    <location id="light_yellow" x="240" y="180">
      <name x="215" y="150">Yellow</name>
      <label kind="invariant" x="215" y="200">t &lt;= 3</label>
    </location>
    <location id="light_red" x="0" y="180">
      <name x="-15" y="150">Red</name>
      <label kind="invariant" x="-25" y="200">t &lt;= 20</label>
    </location>

    <init ref="light_green"/>

    <transition>
      <source ref="light_green"/>
      <target ref="light_green"/>
      <label kind="synchronisation" x="-110" y="-85">pass!</label>
      <nail x="-70" y="-65"/>
      <nail x="40" y="-65"/>
    </transition>
    <transition>
      <source ref="light_green"/>
      <target ref="light_clearance"/>
      <label kind="guard" x="90" y="-30">t == 17</label>
    </transition>
    <transition>
      <source ref="light_clearance"/>
      <target ref="light_yellow"/>
      <label kind="guard" x="255" y="60">t == 20</label>
      <label kind="assignment" x="255" y="85">t = 0, green = false</label>
    </transition>
    <transition>
      <source ref="light_yellow"/>
      <target ref="light_red"/>
      <label kind="guard" x="95" y="195">t == 3</label>
      <label kind="assignment" x="95" y="220">t = 0</label>
    </transition>
    <transition>
      <source ref="light_red"/>
      <target ref="light_green"/>
      <label kind="guard" x="-150" y="60">t == 20</label>
      <label kind="assignment" x="-150" y="85">t = 0, green = true</label>
    </transition>
  </template>

  <template>
    <name>Vehicle</name>
    <declaration>clock c;</declaration>

    <location id="car_approaching" x="0" y="0">
      <name x="-45" y="-30">Approaching</name>
      <label kind="invariant" x="-25" y="20">c &lt;= 5</label>
    </location>
    <location id="car_waiting" x="220" y="0">
      <name x="190" y="-30">Waiting</name>
    </location>
    <location id="car_crossing" x="440" y="0">
      <name x="405" y="-30">Crossing</name>
      <label kind="invariant" x="415" y="20">c &lt;= 3</label>
    </location>
    <location id="car_done" x="660" y="0">
      <name x="640" y="-30">Done</name>
    </location>

    <init ref="car_approaching"/>

    <transition>
      <source ref="car_approaching"/>
      <target ref="car_waiting"/>
      <label kind="guard" x="80" y="-30">c &gt;= 1</label>
      <label kind="assignment" x="80" y="20">c = 0</label>
    </transition>
    <transition>
      <source ref="car_waiting"/>
      <target ref="car_crossing"/>
      <label kind="synchronisation" x="300" y="-30">pass?</label>
      <label kind="assignment" x="300" y="20">c = 0</label>
    </transition>
    <transition>
      <source ref="car_crossing"/>
      <target ref="car_done"/>
      <label kind="guard" x="520" y="-30">c &gt;= 2</label>
    </transition>
  </template>

  <system>
Light = TrafficLight();
Car = Vehicle();
system Light, Car;
  </system>
</nta>
```
```css
A[] not deadlock
A[] (Car.Crossing imply green)
A<> Car.Done
E<> Car.Done
```
