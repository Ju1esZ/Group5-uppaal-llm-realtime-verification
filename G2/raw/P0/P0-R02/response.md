```xml
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE nta PUBLIC "-//Uppaal Team//DTD Flat System 1.1//EN" "http://www.it.uu.se/research/group/darts/uppaal/flat-1_2.dtd">
<nta>
  <declaration>
clock lightClock;
bool green = true;
  </declaration>

  <template>
    <name>TrafficLight</name>
    <declaration></declaration>

    <location id="light_green" x="0" y="0">
      <name x="-20" y="-30">Green</name>
      <label kind="invariant" x="-40" y="20">lightClock &lt;= 20</label>
    </location>
    <location id="light_yellow" x="250" y="0">
      <name x="230" y="-30">Yellow</name>
      <label kind="invariant" x="210" y="20">lightClock &lt;= 3</label>
    </location>
    <location id="light_red" x="125" y="200">
      <name x="110" y="170">Red</name>
      <label kind="invariant" x="85" y="220">lightClock &lt;= 20</label>
    </location>

    <init ref="light_green"/>

    <transition>
      <source ref="light_green"/>
      <target ref="light_yellow"/>
      <label kind="guard" x="60" y="-80">lightClock == 20</label>
      <label kind="assignment" x="40" y="-55">lightClock = 0, green = false</label>
    </transition>
    <transition>
      <source ref="light_yellow"/>
      <target ref="light_red"/>
      <label kind="guard" x="210" y="90">lightClock == 3</label>
      <label kind="assignment" x="210" y="115">lightClock = 0</label>
    </transition>
    <transition>
      <source ref="light_red"/>
      <target ref="light_green"/>
      <label kind="guard" x="-100" y="90">lightClock == 20</label>
      <label kind="assignment" x="-160" y="115">lightClock = 0, green = true</label>
    </transition>
  </template>

  <template>
    <name>Vehicle</name>
    <declaration>
clock carClock;
    </declaration>

    <location id="car_approaching" x="0" y="0">
      <name x="-40" y="-30">Approaching</name>
      <label kind="invariant" x="-40" y="20">carClock &lt;= 5</label>
    </location>
    <location id="car_waiting" x="250" y="0">
      <name x="225" y="-30">Waiting</name>
    </location>
    <location id="car_crossing" x="500" y="0">
      <name x="470" y="-30">Crossing</name>
      <label kind="invariant" x="460" y="20">carClock &lt;= 3</label>
    </location>
    <location id="car_done" x="750" y="0">
      <name x="735" y="-30">Done</name>
    </location>

    <init ref="car_approaching"/>

    <transition>
      <source ref="car_approaching"/>
      <target ref="car_waiting"/>
      <label kind="guard" x="55" y="-80">carClock &gt;= 1 &amp;&amp; carClock &lt;= 5</label>
    </transition>

    <!-- 仅在绿灯剩余时间严格大于 3 秒时允许进入，
         保证整个穿越过程均处于绿灯阶段。 -->
    <transition>
      <source ref="car_waiting"/>
      <target ref="car_crossing"/>
      <label kind="guard" x="285" y="-80">green &amp;&amp; lightClock &lt; 17</label>
      <label kind="assignment" x="330" y="-55">carClock = 0</label>
    </transition>

    <transition>
      <source ref="car_crossing"/>
      <target ref="car_done"/>
      <label kind="guard" x="530" y="-80">carClock &gt;= 2 &amp;&amp; carClock &lt;= 3</label>
    </transition>
  </template>

  <system>
Light = TrafficLight();
Car = Vehicle();
system Light, Car;
  </system>

  <queries/>
</nta>
```
```css
A[] not deadlock
A[] (Car.Crossing imply Light.Green)
E<> Car.Done
A<> Car.Done
Car.Waiting --> Car.Done
```
