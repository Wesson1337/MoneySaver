import React from 'react';
import {ACCOUNT_TYPES, CURRENCIES_AND_SYMBOLS, INTERFACE_COLORS} from "../../utils/consts";
import {prettifyFloat} from "../../utils/prettifyFloat";

const Transaction = ({icon, category, type, amount, amountInAccountCurrency, account, date}) => {
    return (
        <div className="d-flex gap-2 align-items-center">
            <img
                src={icon}
                style={{height: "40px"}}
                alt=""
            />
            <div className="w-100">
                <div className="d-flex justify-content-between gap-3">
                    <p className="m-0 little-text text-nowrap">
                        {category}
                    </p>
                    <p className="m-0 little-text text-nowrap">
                        {type === "spending" ? "-" : "+"}{amount !== amountInAccountCurrency ? prettifyFloat(amountInAccountCurrency.toFixed(2)) : prettifyFloat(amount.toFixed(2))} {CURRENCIES_AND_SYMBOLS[account["currency"]]}
                    </p>
                </div>
                <div className="d-flex justify-content-between gap-3">
                    <p className="m-0 little-text text-nowrap">
                        {`${account["name"] ? account["name"] : "Unnamed account"} (${ACCOUNT_TYPES[account["type"]].name})`}
                    </p>
                    <p className="m-0 little-text text-nowrap">
                        {new Date(date).toLocaleDateString("ru-RU", {hour: "2-digit", minute: "2-digit"})}
                    </p>
                </div>
            </div>
            <div style={{
                width: "5px",
                height: "40px",
                background: type === "spending" ? INTERFACE_COLORS.RED : INTERFACE_COLORS.GREEN
            }}>
            </div>
        </div>
    );
};

export default Transaction;