import React, { Component } from "react";
import ReactEcharts from "echarts-for-react";


class Charts extends Component {

    state = {
        temperatures: null,
        pressure: null,
        wind_speed: null,
        humidity: null,
        xAxis: null,
    }

    getChartColor(type) {
        switch(type){
            case 'Temperatures':
                return "#e91e63"
            case 'Pressures':
                return "#91cc75"
            case 'Wind speed':
                return "#fac858"
            case 'Humidity':
                return "#73c0de"
        }
    }

    componentDidMount() {
        if (this.props.reports !== undefined) {
            this.setOptions(this.props.reports)
        }
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (this.props !== prevProps)
            this.setOptions(this.props.reports)
    }

    setOptions (reports) {
        let xAxis = [];
        Object.keys(reports).map(date => {
            Object.keys(reports[date]).map(hour => {
                xAxis.push(`${date}-${hour}:00`)
            });
        });

        let temperatures = [];
        let pressure = [];
        let wind_speed = [];
        let humidity = [];
        Object.keys(reports).map(date => {
            Object.keys(reports[date]).map(hour => {
                const params = reports[date][hour];
                temperatures.push(parseInt(params.temperature));
                pressure.push(parseInt(params.pressure));
                wind_speed.push(parseInt(params.wind_speed));
                humidity.push(parseInt(params.humidity));
            });
        });
        this.setState({
            temperatures,
            pressure,
            wind_speed,
            humidity,
            xAxis
        })
    }

    getOptions = (data, type) => {
        return {
            title: {
            text: type,
            },
            color: this.getChartColor(type),
            tooltip: {
                trigger: 'axis'
            },
            grid: {
                left: '5%',
                right: '15%',
                bottom: '10%'
            },
            xAxis: [
                {
                  axisLabel: {
                    interval: 3,
                    rotate: 55,
                    textStyle: {
                      baseline: "top",
                      color: "#333",
                      fontSize: 9,
                    },
                    margin: 0,
                    height: 1000
                  },
                  axisLine: { lineStyle: { color: "#aaa" }, show: true },
                  axisTick: { show: false },
                  data: this.state.xAxis,
                  splitLine: { show: false },
                  type: "category"
                }
            ],
            yAxis: { type: "value" },
            toolbox: {
                right: 10,
                feature: {
                    dataZoom: {
                        yAxisIndex: 'none'
                    },
                    restore: {},
                    saveAsImage: {}
                }
            },
            dataZoom: [
                {
                    type: 'slider'
                }
            ],
            series: [
                {
                    data: data,
                    type: "line",
                },
            ],
        };
    };


    render() {
        if (this.state.xAxis == null)
            return null;
        return (
            <div>
                <ReactEcharts style={{ height: "80vh"}}
                              option={this.getOptions(this.state.temperatures, 'Temperatures')}
                />
                <ReactEcharts style={{ height: "80vh"}}
                              option={this.getOptions(this.state.pressure, 'Pressures')}
                />
                <ReactEcharts style={{ height: "80vh"}}
                              option={this.getOptions(this.state.wind_speed, 'Wind speed')}
                />
                <ReactEcharts style={{ height: "80vh"}}
                              option={this.getOptions(this.state.humidity, 'Humidity')}
                />
            </div>
        )
    }
}

export default Charts;