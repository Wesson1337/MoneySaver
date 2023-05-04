import React from 'react';
import {CURRENCIES_AND_SYMBOLS} from "../../utils/consts";
import {ProgressBar} from "react-bootstrap";
import {prettifyFloat} from "../../utils/prettifyFloat";

const Currency = ({currency, percent, balance}) => {
    return (
        <div>
            <div className="d-flex justify-content-between align-items-center w-100 gap-4">
                <p className="m-0">{currency}</p>
                <p className="m-0 little-text">{prettifyFloat(balance.toFixed(2))} {CURRENCIES_AND_SYMBOLS[currency]}</p>
            </div>
            <div
                className="d-flex justify-content-between align-items-center gap-4 w-100"
            >
                <ProgressBar
                    now={percent}
                    style={{height: "3px"}}
                    className="w-100"
                />
                <p
                    className="m-0 text-nowrap little-text"
                    style={{minWidth: "60px", textAlign: "right"}}
                >{percent} %</p>
            </div>
        </div>
    );
};

export default Currency;