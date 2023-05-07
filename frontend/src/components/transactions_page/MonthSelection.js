import React from 'react';
import {Card} from "react-bootstrap";
import arrowLeft from "../../static/icons/arrow-left-334-svgrepo-com.svg"
import arrowRight from "../../static/icons/arrow-right.svg"

const MonthSelection = ({month, setMonth}) => {
    const getDateFromMonth = () => {
        const date = new Date()
        date.setMonth(month)
        return date
    }

    return (
        <Card className="mt-3 p-2 d-flex justify-content-between align-items-center flex-row">
            <div
                className="px-4 py-2 transaction-find-arrow"
                onClick={() => setMonth(month - 1)}
            >
                <img
                    src={arrowLeft}
                    alt=""
                    width={20}
                    style={{userSelect: "none"}}
                />
            </div>
            <h4 className="m-0">{getDateFromMonth().toLocaleDateString("en-UK", {month: "long", year: "numeric"})}</h4>
            <div
                className="px-4 py-2 transaction-find-arrow"
                onClick={() => {
                    if (month < (new Date().getMonth())) {
                        setMonth(month + 1)
                    }
                }}
            >
                <img
                    src={arrowRight}
                    alt=""
                    width={20}
                    style={{userSelect: "none"}}
                />
            </div>
        </Card>
    );
};

export default MonthSelection;