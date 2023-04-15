import React from 'react';
import MainPageCard from "./MainPageCard";
import {CURRENCIES_AND_SYMBOLS, INTERFACE_COLORS, OPERATIONS_ROUTE} from "../../utils/consts";
import {Bar, BarChart, CartesianGrid, Legend, Tooltip, XAxis, YAxis} from "recharts";

const LastSevenDaysOperationsCard = ({data, setErrorMsg}) => {
    const data1 = [
        {
            name: "15.04.2023",
            Spendings: 4000,
            Incomes: 2400,
        },
    ]
    return (
        <MainPageCard navigateto={OPERATIONS_ROUTE} className="mt-3">
            <b>Last 7 days</b>
            <div style={{width: "100%", height: "300px"}}>
                <BarChart
                    width={600}
                    height={300}
                    data={data1}
                    margin={{
                        top: 5,
                        right: 30,
                        left: 20,
                        bottom: 5
                    }}
                >
                    <CartesianGrid strokeDasharray="3 3"/>
                    <XAxis dataKey="name"/>
                    <YAxis unit={CURRENCIES_AND_SYMBOLS.USD}/>
                    <Tooltip/>
                    <Legend/>
                    <Bar dataKey="Incomes" fill={INTERFACE_COLORS.GREEN}/>
                    <Bar dataKey="Spendings" fill={INTERFACE_COLORS.RED}/>
                </BarChart>
            </div>
        </MainPageCard>
    );
};

export default LastSevenDaysOperationsCard;