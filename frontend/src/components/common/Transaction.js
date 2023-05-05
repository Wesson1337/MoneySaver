import React from 'react';
import {ACCOUNT_TYPES, CURRENCIES_AND_SYMBOLS, INTERFACE_COLORS, TRANSACTIONS_ROUTE} from "../../utils/consts";
import {prettifyFloat} from "../../utils/prettifyFloat";
import dots from "../../static/icons/menu-dots-vertical.svg"
import {useLocation} from "react-router-dom";
import {Dropdown} from "react-bootstrap";

const Transaction = ({icon, category, type, amount, amountInAccountCurrency, account, date}) => {
    const location = useLocation()
    const isTransactionPage = location.pathname === TRANSACTIONS_ROUTE
    return (
        <div className="d-flex gap-2 align-items-center">
            <img
                src={icon}
                style={{height: "40px"}}
                alt=""
            />
            <div className="w-100">
                <div className="d-flex justify-content-between align-items-center gap-3">
                    <p className="m-0 little-text text-nowrap">
                        {category}
                    </p>
                    <p className="m-0 little-text text-nowrap">
                        {type === "spending" ? "-" : "+"}{amount !== amountInAccountCurrency ? prettifyFloat(amountInAccountCurrency.toFixed(2)) : prettifyFloat(amount.toFixed(2))} {CURRENCIES_AND_SYMBOLS[account["currency"]]}
                    </p>
                </div>
                <div className="d-flex justify-content-between align-items-center gap-3">
                    <p className="m-0 little-text">
                        {`${account["name"] ? `${account["name"].substring(0, 12)}${account.name.length > 12 ? "..." : ""}` : "Unnamed account"}`}
                    </p>
                    <p className="m-0 little-text text-nowrap">
                        {new Date(date).toLocaleDateString("ru-RU", {hour: "2-digit", minute: "2-digit"})}
                    </p>
                </div>
            </div>
            {isTransactionPage ?
                <Dropdown>
                    <Dropdown.Toggle
                        className="d-flex justify-content-center align-items-center transaction-three-dots"
                    >
                        <img
                            src={dots}
                            alt=""
                            width={20}
                        />
                        <Dropdown.Menu>
                            <Dropdown.Item>
                                Edit transaction
                            </Dropdown.Item>
                            <Dropdown.Item>
                                Delete transaction
                            </Dropdown.Item>
                        </Dropdown.Menu>
                    </Dropdown.Toggle>
                </Dropdown>
                    : null
            }
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