import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { DomSanitizer } from '@angular/platform-browser';
import { CampService } from '../camp.service';
import * as am4core from "@amcharts/amcharts4/core";
import * as am4charts from "@amcharts/amcharts4/charts";
import am4themes_animated from "@amcharts/amcharts4/themes/animated"
import { any } from '@amcharts/amcharts4/.internal/core/utils/Array';



@Component({
  selector: 'app-model',
  templateUrl: './model.component.html',
  styleUrls: ['./model.component.css']
})
export class ModelComponent implements OnInit {
  inputFields:any;
  inputFieldsGrouped:any;
  inputsList:any=[];
  outputData:any={};
  outputsList:any=[];
  outputFileds:any;
  loading: boolean = false;
  el: any;
  title:any = 'chart ';
  chartType: any = 'Line chart';
  errstatus:boolean = false;
  nIntervId: any;
  chartlist:any=['sectordata', 'subsectordata', 'technologydata','sankeydata']

  constructor(private service: CampService) { }

  ngOnInit(): void {
    //this.loading = true;
    this.getInputFields();
    
  }


  
  /*************************************
          API Communicators
  **************************************/
  getInputFields(): void {
    this.service.getInputFields()
      .then((response) => response.json())
      .then(result => {
          this.inputFields = result;
          

          this.inputsList = [];
          for(var i in this.inputFields){
            this.inputFields[i].value = this.inputFields[i].default;
            this.inputFields[i].condition = JSON.parse(this.inputFields[i].condition);
            this.inputsList.push(this.inputFields[i].default);
          }
        
       // this.getOutput();
        this.inputFieldsGrouped = this.groupBy(this.inputFields, 'inputgroup');
        this.inputFieldsGrouped = this.inputFieldsGrouped.__zone_symbol__value;
        
        for(var i in this.inputFieldsGrouped){
          this.inputFieldsGrouped[i]['items2'] = this.groupBy(this.inputFieldsGrouped[i]['items'], 'level0');
          this.inputFieldsGrouped[i]['items2'] = this.inputFieldsGrouped[i]['items2'].__zone_symbol__value;
          for(var j in this.inputFieldsGrouped[i]['items']){
            this.inputFieldsGrouped[i]['items3'] = this.groupBy(this.inputFieldsGrouped[i]['items'], 'header');
            this.inputFieldsGrouped[i]['items3'] = this.inputFieldsGrouped[i]['items3'].__zone_symbol__value;
          }
        }
        
    });
  }

  getOutputFields(): void {
    this.service.generateOutput()
    .then((response) => response.json())
    .then(result => {
        //this.drawSankey(result);
  });
}

  displayChart(): void {
    (<HTMLDivElement>document.getElementById("output_charts")).style.display = 'block';
    this.service.displayChart()
    .then((response) => response.json())
    .then(result => {
        //this.outputFileds = result.xx;
        this.drawSankey(result);
  });

  

    
  
  }

  getOutput() {
    //(<HTMLDivElement>document.getElementById("output_charts")).style.display = 'none';
    this.title='chart';
    this.loading = true;
    this.outputData = [];
    this.service.setInputFields(this.inputsList)
        .then((response) => response.json())
        .then((result) => { 
          this.loading = false; 
          // alert("Generated! click on Display")
          this.outputData = this.groupBy(result.data, 'group');     
          this.outputData = this.outputData["__zone_symbol__value"];     

    });
    setTimeout(() => {
      this.displayChart();
    },  3000);
    
    
  }

  


  /*************************************
          Input/Output UI Helpers
  **************************************/

  async groupBy(data:any, key:any) {
    const helper:any = {};
    return data.reduce((groups:any,x:any) => {
      if (!helper[x[key]]) {
        helper[x[key]] = {
          group: x[key],
          items: [x],
          };

        groups.push(helper[x[key]]);

      } else { helper[x[key]].items.push(x); }
      
      return groups;
    }, []);
  }


  onInputChange(event: any, row:any) {
    if(row.type=="double"){
      this.errstatus=this.withinRange(row);
    }
    this.inputFields[row.id].value=event.target.value;
    this.inputsList[row.id]=event.target.value;
    this.inputFields[row.id].changed=true;
    //this.getOutput();
  }
  
  withinRange(row:any){
    let max=row.condition.max[1];
    let min=row.condition.min[1];
      if (row.value<=min || row.value>=max){
        return true;
      }
    return false;
  }

  reset(){
    this.title = "chart";
    this.getInputFields();
    (<HTMLDivElement>document.getElementById("output_charts")).style.display = 'none';
    //window.location.reload();
  }
  
 
  drawSankey(data:any){
    am4core.useTheme(am4themes_animated);

    for(var item of this.chartlist){
      var chart = am4core.create("chart_"+item, am4charts.SankeyDiagram);
      chart.exporting.menu = new am4core.ExportMenu();
      chart.data = data[item];
      chart.dataFields.fromName = "from";
      chart.dataFields.toName = "to";
      chart.dataFields.value = "weight";
      chart.dataFields.color = "nodeColor";
      chart.paddingRight = 50;
      chart.paddingTop = 20;
      chart.paddingBottom = 80;
      chart.nodeAlign = "bottom";

      // Add title
      this.title = data.title; 
  
      // Configure links
      var linkTemplate = chart.links.template;
      linkTemplate.fontSize = 20;
      linkTemplate.tooltipText = " [font-size: 20px]{fromName} → {toName}: [bold font-size: 30px]{value}[/] [font-size: 20px]GtCO2e[/]\n[font-size: 20px]{fromName} contribute [bold font-size: 30px]{value2} [/] [font-size: 20px]% in {toName}[/] ";
      linkTemplate.colorMode = "gradient";
      // linkTemplate.colorMode = "fromNode";
      // linkTemplate.fillOpacity = 1;
      // linkTemplate.strokeOpacity = 1;
      // linkTemplate.tension = 1;
      // linkTemplate.controlPointDistance = 0.1;
      // linkTemplate.fill = am4core.color("#A8C686");
      
      let nodeTemplate = chart.nodes.template;
      nodeTemplate.nameLabel.label.fontSize = 14;
      nodeTemplate.nameLabel.label.truncate = false;
      // nodeTemplate.nameLabel.label.wrap = true;
      // nodeTemplate.width = 30;
      // nodeTemplate.minHeight = 30;

      var hoverState = linkTemplate.states.create("hover");
      hoverState.properties.fillOpacity = 1;

      // Configure nodes
      nodeTemplate.cursorOverStyle = am4core.MouseCursorStyle.pointer;
      nodeTemplate.readerTitle = "Click to show/hide or drag to rearrange";
      nodeTemplate.showSystemTooltip = true;
      
    }
    
  }
  
}
