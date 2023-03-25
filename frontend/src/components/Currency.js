import React from 'react';
import {CURRENCIES_AND_SYMBOLS} from "../utils/consts";
import {ProgressBar} from "react-bootstrap";

const Currency = (props) => {
    return (
        <div>
            <div className="d-flex justify-content-between align-items-center w-100 gap-4">
                <p className="m-0">{props.currency}</p>
                <p className="m-0 little-text">{props.balance.toFixed(2)} {CURRENCIES_AND_SYMBOLS[props.currency]}</p>
            </div>
            <div
                className="d-flex justify-content-between align-items-center gap-4 w-100"
            >
                <ProgressBar
                    now={props.percent}
                    style={{height: "3px"}}
                    className="w-100"
                />
                <p
                    className="m-0 text-nowrap little-text"
                    style={{minWidth: "35.5px", textAlign: "right"}}
                >{props.percent} %</p>
            </div>
        </div>
    );
};

export default Currency;