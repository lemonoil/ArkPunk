<template>
  <div class='main'>
  <div style="font-size: 25px;text-align: center;color: white;">
            明日方舟伤害治疗统计</div>
            <br><br><br><br><br>
 <el-radio-group v-model="radio" size="medium">
  <el-radio-button :label="1">条形图</el-radio-button>
  <el-radio-button :label="2">折线图</el-radio-button>
  </el-radio-group>
 <el-button  icon="el-icon-delete-solid" size="medium" @click="clear">清空</el-button> 
 <div class="charts">
  <ve-bar :data="barChartData" :settings="barChartSettings" :extend="barChartExtend" v-if="radio===1"></ve-bar>
  <ve-line :data="lineChartData" :extend="lineChartSettings" v-if="radio===2"></ve-line>
 </div>
  </div>
</template>

<script>
  import "echarts/lib/component/title";
  import 'echarts/lib/component/markLine'
  import 'echarts/lib/component/markPoint'

  import axios from 'axios';
  import io from 'socket.io-client';
  export default {
    data () {
      this.barChartSettings = { 
        stack:{ 'xxx': ['物理伤害', '法术伤害','真实伤害','治疗回复','友方伤害'] },
        dataOrder:{label:'total', order:'desc'}
      },
      this.barChartExtend = {
        'xAxis.0.axisLabel.color': 'white',
        'yAxis.0.axisLabel.color': "white",
        color: ['#60B9F4','#6C6CE8', '#071B07', '#33CC33','#888888'],
        legend: {
          textStyle: {
            color: 'white',
          }
        }
      },
      this.lineChartSettings = {
        'xAxis.0.axisLabel.color': 'white',
        'yAxis.0.axisLabel.color': "white",
        legend: {
          textStyle: {
            color: 'white',
          }
        }
      },
      this.lineTimerMap = {},
      this.lineTimerCnt = 0
      return {
        barChartData: {
          columns: ['名称', '物理伤害', '法术伤害','真实伤害','治疗回复','友方伤害'],
          rows: []
        },
        lineChartData: {
          columns: ['时间'],
          rows: []
        },
        radio: 2,
      }
    },
    created: function(){
      this.startTime = Date.now();
      setInterval(this.pushLineData, 1500);
      const socket = io('http://127.0.0.1:9081');
      socket.on('confirm_connection',(data) => {
          console.log('conection status: '+data['msg'])
      });
      socket.on('damageData', (data) => {
          console.log(data['val']);
          console.log(data['type']);
          var idx = -1
          for(var i=0;i<this.lineChartData.columns.length;i++) {
            if(this.lineChartData.columns[i] === data['名称'])
              idx=i-1;
          }
          if( idx === -1){
            let pushData = { '名称': '', '物理伤害':0, '法术伤害':0, '真实伤害':0,'治疗回复':0,'友方伤害':0,'total': 0};
            pushData['名称'] = data['名称'];
            this.barChartData.rows.push(pushData);
            this.lineChartData.columns.push(data['名称']);
            for(var i=0;i<this.lineTimerCnt;i++){
              this.lineChartData.rows[i][data['名称']] = 0;
            }
            idx = this.barChartData.rows.length - 1;
          }
          this.barChartData.rows[idx][data['type']] += data['val'];
          this.barChartData.rows[idx]['total'] += data['val'];
          if(this.lineTimerMap[data['名称']] == undefined) this.lineTimerMap[data['名称']] = data['val'];
          else this.lineTimerMap[data['名称']] += data['val'];

      });

    },
    methods: {
        clear: function() {
          this.barChartData.rows = [];
          this.lineChartData.columns = ['时间'];
          this.lineChartData.rows = [];
          this.lineTimerMap = {};
          this.lineTimerCnt = 0;
        },
        pushLineData: function() {
          for(var i=1;i<this.lineChartData.columns.length;i++){
            let charter = this.lineChartData.columns[i];
            if(this.lineTimerMap[charter] === undefined){
              this.lineTimerMap[charter] = 0;
            }
          }
          this.lineTimerMap['时间'] = this.lineTimerCnt++;;
          this.lineChartData.rows.push(this.lineTimerMap);
          this.lineTimerMap={};
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
.el-button {
    font-size: 12px;
    margin: 15px;
}
.el-button--primary:focus, .el-button--primary:hover {
    background: #42e165;
    border-color: #42e149;
    color: #FFF;
}
.el-radio-group{
    margin: 15px;
}
</style>