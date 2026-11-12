```xml
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE nta PUBLIC '-//Uppaal Team//DTD Flat System 1.1//EN' 'http://www.it.uu.se/research/group/darts/uppaal/flat-1_2.dtd'>
<nta>
  <declaration>
clock phase;
bool green = true;
  </declaration>

  <template>
    <name>TrafficLight</name>
    <declaration></declaration>

    <location id="light_green" x="0" y="0">
      <name x="-20" y="-30">Green</name>
      <label kind="invariant" x="-30" y="20">phase &lt;= 20</label>
    </location>
    <location id="light_yellow" x="250" y="0">
      <name x="225" y="-30">Yellow</name>
      <label kind="invariant" x="220" y="20">phase &lt;= 3</label>
    </location>
    <location id="light_red" x="125" y="200">
      <name x="110" y="170">Red</name>
      <label kind="invariant" x="95" y="220">phase &lt;= 20</label>
    </location>

    <init ref="light_green"/>

    <transition>
      <source ref="light_green"/>
      <target ref="light_yellow"/>
      <label kind="guard" x="75" y="-60">phase == 20</label>
      <label kind="assignment" x="60" y="-35">phase = 0, green = false</label>
    </transition>
    <transition>
      <source ref="light_yellow"/>
      <target ref="light_red"/>
      <label kind="guard" x="200" y="80">phase == 3</label>
      <label kind="assignment" x="200" y="105">phase = 0</label>
    </transition>
    <transition>
      <source ref="light_red"/>
      <target ref="light_green"/>
      <label kind="guard" x="-90" y="80">phase == 20</label>
      <label kind="assignment" x="-140" y="105">phase = 0, green = true</label>
    </transition>
  </template>

  <template>
    <name>Vehicle</name>
    <declaration>clock c;</declaration>

    <location id="car_approaching" x="0" y="0">
      <name x="-40" y="-30">Approaching</name>
      <label kind="invariant" x="-20" y="20">c &lt;= 5</label>
    </location>
    <location id="car_waiting" x="250" y="0">
      <name x="220" y="-30">Waiting</name>
    </location>
    <location id="car_crossing" x="500" y="0">
      <name x="470" y="-30">Crossing</name>
      <label kind="invariant" x="480" y="20">c &lt;= 3</label>
    </location>
    <location id="car_done" x="750" y="0">
      <name x="730" y="-30">Done</name>
    </location>

    <init ref="car_approaching"/>

    <transition>
      <source ref="car_approaching"/>
      <target ref="car_waiting"/>
      <label kind="guard" x="80" y="-60">c &gt;= 1 &amp;&amp; c &lt;= 5</label>
    </transition>
    <transition>
      <source ref="car_waiting"/>
      <target ref="car_crossing"/>
      <label kind="guard" x="300" y="-60">green &amp;&amp; phase &lt; 17</label>
      <label kind="assignment" x="345" y="-35">c = 0</label>
    </transition>
    <transition>
      <source ref="car_crossing"/>
      <target ref="car_done"/>
      <label kind="guard" x="565" y="-60">c &gt;= 2 &amp;&amp; c &lt;= 3</label>
    </transition>
  </template>

  <system>
Light = TrafficLight();
Car = Vehicle();
system Light, Car;
  </system>

  <queries>
    <query>
      <formula>A[] not deadlock</formula>
      <comment>系统始终无死锁。</comment>
    </query>
    <query>
      <formula>A[] (Car.Crossing imply Light.Green)</formula>
      <comment>车辆穿越期间始终为绿灯；仅在绿灯剩余时间大于 3 秒时允许进入路口。</comment>
    </query>
    <query>
      <formula>E&lt;&gt; Car.Done</formula>
      <comment>存在车辆完成通行的执行路径。</comment>
    </query>
  </queries>
</nta>
```
```css
A[] not deadlock
A[] (Car.Crossing imply Light.Green)
E<> Car.Done
```
