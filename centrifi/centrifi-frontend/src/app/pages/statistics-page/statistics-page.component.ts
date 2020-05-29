import { Component, OnInit } from '@angular/core';
import { DataService } from 'src/app/shared/data.service';
import { NetworkStats, Traffic, Day, Month } from 'src/app/shared/network-stats';
import { RouterStatLines } from 'src/app/shared/router-stat-lines';
import { NgxStatLine, Series } from 'src/app/shared/ngx-stat-line';
import { NetworkInfo } from 'src/app/shared/network-info';
import { DatePipe } from '@angular/common';
import { FormControl } from '@angular/forms';


const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
  "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"
];

@Component({
  selector: 'app-statistics-page',
  templateUrl: './statistics-page.component.html',
  styleUrls: ['./statistics-page.component.css']
})
export class StatisticsPageComponent implements OnInit {

  breadthOptions: Array<string> = ["Entire Network"];

  readonly intervalOptions: Array<string> = ["Hour", "Day", "Month"];
  readonly dataSizeOption: Map<string, number> = new Map([
    ['Bytes', 1],
    ['Kilobytes', 1000],
    ['Megabytes', 1000000],
    ['Gigabytes', 1000000000],
  ]);

  // Flags
  dataCouldNotBeReceived: boolean = false;
  dataProcessed: boolean = false;
  dataMismatch: boolean = false; // Network info and stat data does not match
  
  // Raw Data
  stats:NetworkStats;
  networkInfo: NetworkInfo;

  // Formatted data
  formattedStats: Map<string,RouterStatLines> = new Map<string,RouterStatLines>();
  
  // User Selection
  selectedBreadth:FormControl = new FormControl([this.breadthOptions[0]]);
  selectedInterval:string = this.intervalOptions[0];
  activeStats: Array<NgxStatLine> = new Array<NgxStatLine>();

  // Currently no user selections, but option to add in future is there
  dataSize:string = this.dataSizeOption.entries().next().value[0];
  dataSizeNumber:number = this.dataSizeOption.entries().next().value[1];

  // Graph Options
    legend: boolean = true;
    legendTitle: string = "Network Area"
    legendPosition: string = "below";
    showLabels: boolean = true;
    animations: boolean = true;
    xAxis: boolean = true;
    yAxis: boolean = true;
    showYAxisLabel: boolean = true;
    showXAxisLabel: boolean = true;
    xAxisLabel: string = 'Time';
    yAxisLabel: string = 'Data in ' + this.dataSize;
    timeline: boolean = true;

    colorScheme = {
      domain: ['#5AA454', '#E44D25', '#CFC0BB', '#7aa3e5', '#a8385d', '#aae3f5']
    };  

  constructor(
    private dataService: DataService,
    private datePipe: DatePipe
  ) { }


  //
  // On component creation, initial setup
  //

  ngOnInit(): void {
    this.dataService.getNetworkStatistics().subscribe((response)=>{
      let data = response.body;
      
      this.dataCouldNotBeReceived = false;
      this.stats = <NetworkStats> data;
      this.getNetworkInfo();
    },
    error=>{
      this.dataCouldNotBeReceived = true;
      console.error("Cannot make request");
    });
  }

  getNetworkInfo(){
    this.dataService.getNetworkInfo().subscribe((response)=>{
      let data = response.body;

      this.networkInfo = <NetworkInfo> data;
      this.dataReceivedTasks();
    },
    error=>{
      this.dataCouldNotBeReceived = true;
      console.error("Cannot make network info request");
    });
  }
  
  // Function that takes data received and formats it into
  // data readable by the NGX Charts Module
  dataReceivedTasks(){
    if(!this.checkForDataMismatch()){
      this.createOptions();
      this.createLines()
      this.changeActiveStats();
      this.dataProcessed = true;  
    }
  }

  // Creates a list of options for each 
  createOptions(){
    this.networkInfo.aps.forEach(ap => {
      this.breadthOptions.push(this.dataService.getRouterWholeName(this.networkInfo, ap.apIP))
    })
  }

  // Checks whether the list of AP's from get-network-info is the same
  // as the list provided in statistics info
  checkForDataMismatch(): boolean{
    console.log(this.networkInfo)
    console.log(this.networkInfo.aps.length)
    console.log(this.formattedStats)
    console.log(this.formattedStats.size-1)


    // Checks if data size is different
    if(this.networkInfo.aps.length !== this.stats.routerStats.length){
      this.dataMismatch = true;
      console.log("size mismatch");
      return true;
    }

    // Checks if each individual access point option is available
    this.networkInfo.aps.forEach(ap => {
      if(!this.stats.routerStats.find(routerstat => ap.apIP === routerstat.routerIP)){
        this.dataMismatch = true;
        console.log("data mismatch")
        return true;
      }
    });
    return false;
  }

  //
  // React to user input
  //

  onBack(){
    this.dataService.goToHomePage();
  }

  onDataSelection(){
    this.changeActiveStats();
  }

  // Moves inactive data stored in this.formattedStats, to
  // the active stats as necessary 
  changeActiveStats(){
    this.activeStats = [];

    // Get the names of all selected access points
    let selectedAps: Array<string> = this.selectedBreadth.value;
    
    // TODO copy before pushing
    selectedAps.forEach(selectedAp => {
      if(this.selectedInterval == "Hour"){
        this.activeStats.push(this.formattedStats.get(selectedAp).rxHourLine);
        this.activeStats.push(this.formattedStats.get(selectedAp).txHourLine);
      }
      else if(this.selectedInterval == "Day") {
        this.activeStats.push(this.formattedStats.get(selectedAp).rxDayLine);
        this.activeStats.push(this.formattedStats.get(selectedAp).txDayLine);
      }
      else if(this.selectedInterval == "Month"){
        this.activeStats.push(this.formattedStats.get(selectedAp).rxMonthLine);
        this.activeStats.push(this.formattedStats.get(selectedAp).txMonthLine);
      }
    });
  }




  //
  // Process initial data
  //

  // Function that takes the raw statistic data and converts it into the line
  // formate needed by the NGX chart 
  createLines(){
    // For whole network
    let wholeNetworkStat = this.stats.routerStats[0].rawVnstat.interfaces.find(tInterface => tInterface.id ==="eth0.2").traffic;

    this.formattedStats.set(
      this.breadthOptions[0],
      // We need to swap this tx and rx data, because all downstream traffic 
      // for the WAN port is actually upstream traffic for the rest of the network
      this.createRouterStatLines(this.breadthOptions[0], wholeNetworkStat, true)
    )

    // For each individual router
    this.stats.routerStats.forEach(routerStat => {
      console.log("Creating for routerstat:")
      console.log(routerStat)
      let statSeriesName = this.dataService.getRouterWholeName(this.networkInfo, routerStat.routerIP);
      let routerInterface = routerStat.rawVnstat.interfaces.find(tInterface => tInterface.id ==="wlan1");
      console.log("Found interface data:")
      console.log(routerInterface)
      if(routerInterface){
        this.formattedStats.set(statSeriesName, this.createRouterStatLines(statSeriesName, routerInterface.traffic, false));
      }
    })
    console.log("Updated formatted stats to: ")
    console.log(this.formattedStats)
  }

  // Creates and returns collection of 6 NGX line, upload and download for each
  // of the three units of time that the raw statistics data provides 
  createRouterStatLines(statLineName: string, traffic:Traffic, swapTxAndRx:boolean): RouterStatLines{
    // If we are swapping Tx and Rx then we need to swap which
    // data the convert to lines is pulling from so that rx data
    // is converted to tx and vice versa
    let txflag = !swapTxAndRx // (swapTxAndRx ? false : true)

    return {
      name: statLineName,
      txHourLine: this.convertToLines("hours", statLineName, traffic, swapTxAndRx, txflag),
      txDayLine: this.convertToLines("days", statLineName, traffic, swapTxAndRx, txflag),
      txMonthLine: this.convertToLines("months", statLineName, traffic, swapTxAndRx, txflag),
      rxHourLine: this.convertToLines("hours", statLineName, traffic, swapTxAndRx, !txflag),
      rxDayLine: this.convertToLines("days", statLineName, traffic, swapTxAndRx, !txflag),
      rxMonthLine: this.convertToLines("months", statLineName, traffic, swapTxAndRx, !txflag )
    }
  }

  // Takes a singular line of statistic data and returns an NGX line for it
  convertToLines(lineType: string,name: string, traffic:Traffic, swapTxAndRx:boolean, tx: boolean): NgxStatLine{
    let series: Array<Series>;

    if(lineType === "hours"){
        series = this.createHourSeriesItems(traffic["hours"], tx)
    }
    else if(lineType === "days"){
      series = this.createDaySeriesItems(traffic["days"], tx)
    }
    else if(lineType === "months"){
      series = this.createMonthSeriesItems(traffic["months"], tx)
    }
    
    let NgxStatLine: NgxStatLine = {
      // If we are swapping the tx and rx, swap the name
      name: this.appendToName(name,(swapTxAndRx ? !tx : tx)),
      series: series
    }
    return NgxStatLine;
  }

  // Adds up or down to a the router IP so that the data it represents is
  // represented correctly
  appendToName(name: string, tx: boolean): string{
    return (tx ? "Up - " + name : "Down - " + name);
  }

  // Creates hour series items by changing date to proper form
  createHourSeriesItems(rawItems: Array<Day>, tx: boolean):Array<Series>{
    let series = new Array<Series>();
    rawItems.forEach(item => {
      // Since last 24 hours are kept based on ID the UTC hour they correspond to
      // we need to create a new UTC string (plus 1 to month because JS UTC month
      // is on 0-11 scale)
      let date: Date = new Date(Date.UTC(item.date.year, item.date.month + 1, item.date.day, item.id));
      
      let dateString = this.datePipe.transform(date, "L/d - H:00");
      ;

      // Get proper item
      let value: number = (tx ? item.tx : item.rx) 

      // Insert at the beginning of the array since newer times come first in vnstat
      series.push(this.createSeriesItem(dateString, value));
    });

    series.sort(function(a:Series, b:Series) {
      return a.name.localeCompare(b.name);
    })

    return series;
  }

  // Creates day series items by changing date to proper form
  createDaySeriesItems(rawItems: Array<Day>, tx: boolean):Array<Series>{
    let series = new Array<Series>();
    rawItems.forEach(item => {
      // Since last 30 days are kept based on date
      let date: string =
        this.datePipe.transform(new Date(item.date.year, item.date.month-1, item.date.day), "MMM d");

      // Get proper item
      let value: number = (tx ? item.tx : item.rx) 

      // Insert at the beginning of the array since newer times come first in vnstat
      series.unshift(this.createSeriesItem(date, value));
    });
    
    return series;
  }

  // Creates month series items by changing date to proper form
  createMonthSeriesItems(rawItems: Array<Month>, tx: boolean):Array<Series>{
    let series = new Array<Series>();
    rawItems.forEach(item => {
      // Since last 12 months with 1-12 indexing
      let date: string = monthNames[item.date.month-1];
      
      // Get proper item
      let value: number = (tx ? item.tx : item.rx) 
      
      // Insert at the beginning of the array since newer times come first in vnstat
      series.unshift(this.createSeriesItem(date, value));
    });
    return series;
  }

  // Creates NGX statline series item given a name and a value
  createSeriesItem(name: string, value: number): Series{
    return { name: name, value: value }
  }
}
