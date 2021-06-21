import React, { Component } from "react";
import Content from "./components/Charts";
import Header from './components/Header';


class App extends Component {
    render() {

        return (
            <div>
                <Header/>
                <Content/>
            </div>
        );
    }
}
export default App;
