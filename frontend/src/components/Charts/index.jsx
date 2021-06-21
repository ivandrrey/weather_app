import React, { Component } from "react";
import styles from "./Charts.module.css"
import Charts from "./Chart"


class Content extends Component {

    state = {
        loader: true,
        countries: null,
        minDate: null,
        maxDate: null,
        choosedCountry: null,
        choosedCity: null,
        reportData: null
    }

    maxDateForInput = this.getFormatedDate(new Date());

    componentDidMount() {
        fetch('http://localhost:8000/api/get-data-form/', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json;charset=utf-8'
                },
        }).then(response => {
            if ([500, 504, 401, 403, 404].includes(response.status))
                return Promise.reject({type: 'redirect', status: response.status});
            return response.json();
        }).then(data => {
            this.setState({
                loader: false,
                countries: data
            });
        }).catch(e => console.log(e));
        this.setState({minDate: this.maxDateForInput, maxDate: this.maxDateForInput})
    }

    getReportData() {
        this.setState({loader: true});
        const {minDate, maxDate, choosedCity} = this.state;
        fetch(`http://localhost:8000/api/get-report-data/?city_id=${choosedCity}&start_date=${minDate}&end_date=${maxDate}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json;charset=utf-8'
                },
        }).then(response => {
            if ([500, 504, 401, 403, 404].includes(response.status))
                return Promise.reject({type: 'redirect', status: response.status});
            return response.json();
        }).then(data => {
            if (data['errors'] !== undefined)
                this.setState({loader: false});
            else
                this.setState({
                    loader: false,
                    reportData: data
                });
        })
    }

    getFormatedDate(date) {
        const year = date.getFullYear();
        let month = date.getMonth() + 1;
        if (month < 10)
            month = `0${month}`;
        let day = date.getDate();
        if (day < 10)
            day = `0${day}`;
        return `${year}-${month}-${day}`
    }

    changeDate(value, type) {
        let newState = {};
        newState[type] = value;
        if (type === 'maxDate' && new Date(value) <= new Date(this.state.minDate)){
            newState['minDate'] = value;
        }
        this.setState(newState);
    }

    render() {
        const {loader, minDate, maxDate, countries, choosedCountry, choosedCity, reportData} = this.state;
        return (
            <div>
                <div>
                    <select className={styles.input}
                            value={choosedCountry}
                            onChange={(e) => this.setState({choosedCountry: e.target.value})}
                    >
                        {choosedCountry == null && <option value={null}>Страна</option>}
                        {countries &&
                            Object.keys(countries).map((name, key) => (
                                <option value={name}>{name}</option>
                        ))}
                    </select>
                    <select className={styles.input}
                            value={choosedCity}
                            onChange={(e) => this.setState({choosedCity: e.target.value})}
                    >
                        {choosedCity == null && <option value={null}>Город</option>}
                        {countries && choosedCountry &&
                            countries[choosedCountry].map((city) => (
                                <option value={city.id}>{city.name}</option>
                        ))}
                    </select>
                    <label>Начиная с </label>
                    <input className={styles.input}
                           type="date" id="start_date"
                           value={minDate}
                           max={maxDate == null? this.maxDateForInput : maxDate}
                           onChange={(e)=> this.changeDate(e.target.value, 'minDate')}
                    />
                    <label> по </label>
                    <input className={styles.input}
                           type="date" id="end_date"
                           value={maxDate}
                           max={this.maxDateForInput}
                           onChange={(e)=> this.changeDate(e.target.value, 'maxDate')}
                    />
                    <button className={styles.input}
                            disabled={choosedCity == null || loader}
                            onClick={() => this.getReportData()}
                    >
                        Показать
                    </button>
                </div>
                {reportData != null &&
                    <Charts reports={reportData}/>
                }
            </div>
        );
    }
}
export default Content;