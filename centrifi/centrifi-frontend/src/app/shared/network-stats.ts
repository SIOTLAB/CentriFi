export interface NetworkStats {
    routerStats: RouterStat[];
}

export interface RouterStat{
    routerIP: string;
    rawVnstat: RawVnstat;
}

export interface RawVnstat{
    vnstatversion: string;
    jsonversion:   string;
    interfaces:    Interface[];    
}

export interface Interface {
    id:      string;
    nick:    string;
    created: Created;
    updated: Updated;
    traffic: Traffic;
}

export interface Created {
    date: CreatedDate;
}

export interface CreatedDate {
    year:  number;
    month: number;
    day:   number;
}

export interface Traffic {
    total:  Total;
    days:   Day[];
    months: Month[];
    tops:   Day[];
    hours:  Day[];
}

export interface Day {
    id:    number;
    date:  CreatedDate;
    rx:    number;
    tx:    number;
    time?: Time;
}

export interface Time {
    hour:    number;
    minutes: number;
}

export interface Month {
    id:   number;
    date: MonthDate;
    rx:   number;
    tx:   number;
}

export interface MonthDate {
    year:  number;
    month: number;
}

export interface Total {
    rx: number;
    tx: number;
}

export interface Updated {
    date: CreatedDate;
    time: Time;
}
