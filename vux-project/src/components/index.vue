<template>
  <div>
    <div class="home">
      <tabber>
        <tabbar-item link="/index">
          <span slot="icon" class="icon-home"></span>
          <span slot="label">首页</span>
        </tabbar-item>
        <tabbar-item link="/personal" >
          <span slot="icon" class="icon-store"></span>
          <span slot="label">我的</span>
        </tabbar-item>
      </tabber>
    </div>
  </div>
</template>

<script>
import { Tabbar, TabbarItem, Group, Cell } from 'vux'

export default {
  components: {
    Tabbar,
    TabbarItem,
    Group,
    Cell
  },
  data () {
    return {
      msg: 'Hello World!'
    }
  }
}
</script>
<style lang="less">
.home {
  text-align: center;
}
</style>
