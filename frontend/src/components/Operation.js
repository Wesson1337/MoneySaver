import React from 'react';
import {CURRENCIES_AND_SYMBOLS} from "../utils/consts";

const Operation = (props) => {
    return (
        <div className="d-flex gap-2 align-items-center">
            <img
                src={props.icon}
                style={{height: "40px"}}
                alt=""
            />
            <div className="w-100">
                <div className="d-flex justify-content-between">
                    <p className="m-0 little-text">
                        {props.category}
                    </p>
                    <p className="m-0 little-text">
                        {props.type === "spending" ? "-" : "+"}{props.amount} {CURRENCIES_AND_SYMBOLS[props.currency]}
                    </p>
                </div>
                <div className="d-flex justify-content-between">
                    <p className="m-0 little-text">
                        {props.account["type"]}
                    </p>
                    <p className="m-0 little-text">
                        {new Date(props.date).toLocaleDateString("ru-RU", {hour: "2-digit", minute: "2-digit"})}
                    </p>
                </div>
            </div>
        </div>
    );
};

export default Operation;