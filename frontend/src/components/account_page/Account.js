import React from 'react';
import {Card, Form} from "react-bootstrap";
import {CURRENCIES_AND_SYMBOLS} from "../../utils/consts";
import {prettifyFloat} from "../../utils/prettifyFloat";

const Account = ({account, index}) => {

    const handleCheckOnChange = async () => {

    }

    return (
        <Card
            className="p-3 d-flex flex-column gap-2"
        >
            <div className="d-flex justify-content-between">
                <p className="m-0">{account.name}</p>
                <p className="m-0">{prettifyFloat(account.balance.toFixed(2))} {CURRENCIES_AND_SYMBOLS[account.currency]}</p>
            </div>
            <div className="d-flex justify-content-between">
                <Form>
                    <Form.Check
                        id={`account-checkbox-${index !== undefined ? index : 1}`}
                        label={"Active"}
                        type={"switch"}
                        defaultChecked={account["is_active"]}
                    />
                </Form>
                <p className="m-0">{prettifyFloat(account.balance)} {CURRENCIES_AND_SYMBOLS[account.currency]}</p>
            </div>
        </Card>
    );
};

export default Account;