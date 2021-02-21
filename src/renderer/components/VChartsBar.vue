<template>
  <div class='main'>
  <ve-bar :title="{text:'明日方舟伤害统计'}"  :data="chartData" :settings="chartSettings" :extend="chartExtend"></ve-bar>
  <div class='coms'>
  <el-button type="primary" icon="el-icon-delete-solid" @click="clear">清空</el-button>
  </div>
  </div>
  
</template>

<script>
  import "echarts/lib/component/title";
  import "element-ui/lib/button"
  import axios from 'axios';
  import io from 'socket.io-client';
  export default {
    data () {
      this.chartSettings = { 
        stack:{ 'xxx': ['物理伤害', '法术伤害','真实伤害','治疗回复'] },
        dataOrder:{label:'total', order:'desc'}
      },
      this.chartExtend = {
        color: ['#60B9F4','#6C6CE8', '#071B07', '#33CC33',]
      }
      return {
        chartData: {
          columns: ['名称', '物理伤害', '法术伤害','真实伤害','治疗回复'],
          rows: []
        }
      }
    },
    created: function(){
      const socket = io('http://127.0.0.1:9081');
      socket.on('confirm_connection',(data) => {
          console.log('conection status: '+data['msg'])
      });
      socket.on('chartData', (data) => {
          var idx = -1
          for(var i=0;i<this.chartData.rows.length;i++) {
            if(this.chartData.rows[i]['名称'] == data['名称'])
              idx=i;
          }
          console.log()
          if( idx === -1){
            let pushData = { '名称': '', '物理伤害': 0, '法术伤害': 0, '真实伤害':0, '治疗回复':0 , 'total': 0};
            pushData['名称'] = data['名称'];
            this.chartData.rows.push(pushData);
            idx = this.chartData.rows.length - 1;
          }
          this.chartData.rows[idx][data['type']] += data['val'];
          this.chartData.rows[idx]['total'] += data['val'];
      });
    },
    methods: {
        clear: function() {
          this.chartData.rows = []
        }
    },
    mounted() {
      let _this = this; 
      
    }
  }
</script>
<style>
.main{
  margin:35px 75px 75px;
  padding: 3%;
}
</style>