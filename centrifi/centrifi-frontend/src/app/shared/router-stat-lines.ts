import { NgxStatLine } from './ngx-stat-line';

export interface RouterStatLines {
    name: string;
    txHourLine: NgxStatLine;
    txDayLine: NgxStatLine;
    txMonthLine: NgxStatLine;
    rxHourLine: NgxStatLine;
    rxDayLine: NgxStatLine;
    rxMonthLine: NgxStatLine;
}
