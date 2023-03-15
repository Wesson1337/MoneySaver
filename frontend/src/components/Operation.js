import React from 'react';
import {ACCOUNT_TYPES, INTERFACE_COLORS, CURRENCIES_AND_SYMBOLS} from "../utils/consts";

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
                        {props.type === "spending" ? "-" : "+"}{props.amount !== props.amountInAccountCurrency ? props.amountInAccountCurrency : props.amount} {CURRENCIES_AND_SYMBOLS[props.account["currency"]]}
                    </p>
                </div>
                <div className="d-flex justify-content-between">
                    <p className="m-0 little-text">
                        {`${props.account["name"] ? props.account["name"] : "Unnamed account"} (${ACCOUNT_TYPES[props.account["type"]].name})`}
                    </p>
                    <p className="m-0 little-text">
                        {new Date(props.date).toLocaleDateString("ru-RU", {hour: "2-digit", minute: "2-digit"})}
                    </p>
                </div>
            </div>
            <div style={{width: "5px", height: "40px", background: props.type === "spending" ? INTERFACE_COLORS.RED : INTERFACE_COLORS.GREEN}}>
            </div>
        </div>
    );
};

export default Operation;