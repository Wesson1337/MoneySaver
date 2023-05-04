import React, {useEffect, useState} from 'react';
import MainPageCard from "./MainPageCard";
import {INTERFACE_COLORS, OPERATIONS_ROUTE, SUPPORTED_CURRENCIES} from "../../utils/consts";
import {Cell, Pie, PieChart, Tooltip} from "recharts";
import {convertCurrency} from "../../utils/currency";
import {Spinner} from "react-bootstrap";
import green_arrow from "../../static/icons/green_arrow.svg"
import red_arrow from "../../static/icons/red-arrow.svg"
import {prettifyFloat} from "../../utils/prettifyFloat";


const MonthTransactionsCard = (props) => {
    const [isLoading, setIsLoading] = useState(true)
    const [totalIncomeAmount, setTotalIncomeAmount] = useState(0)
    const [totalSpendingAmount, setTotalSpendingAmount] = useState(0)

    const dataForPie = [
        {name: "Incomes", value: totalIncomeAmount, color: INTERFACE_COLORS.GREEN},
        {name: "Spendings", value: totalSpendingAmount, color: INTERFACE_COLORS.RED},
    ];

    const emptyDataForPie = [
        {name: "null", value: 100, color: "grey"}
    ]

    const filterOperationsByMonth = (operations) => {
        let filteredIncomes
        let filteredSpendings
        const date = new Date()
        if (props.month === "this-month") {
            date.setDate(1)
            filteredSpendings = operations.spendings.filter(
                spending => new Date(spending["created_at"]) >= date
            )
            filteredIncomes = operations.incomes.filter(
                income => new Date(income["created_at"]) >= date
            )
        } else {
            date.setDate(1)
            date.setMonth(date.getMonth() - 1)
            filteredSpendings = operations.spendings.filter(
                spending => new Date(spending["created_at"]) >= date
                    && new Date(spending["created_at"]) < new Date(date.getFullYear(), date.getMonth() + 1, 1)
            )
            filteredIncomes = operations.incomes.filter(
                income => new Date(income["created_at"]) >= date
                    && new Date(income["created_at"]) < new Date(date.getFullYear(), date.getMonth() + 1, 1)
            )
        }
        return {incomes: filteredIncomes, spendings: filteredSpendings}
    }

    const getAmountOfOperations = async (operations, type) => {
        let totalAmount = 0
        let convertedAmount
        const account = type === "spendings" ? "receipt_account" : "replenishment_account"
        await operations.map(async op => {
            if (op[account]["currency"] !== SUPPORTED_CURRENCIES.USD) {
                convertedAmount = await convertCurrency(
                    op["amount_in_account_currency_at_creation"],
                    op[account]["currency"],
                    SUPPORTED_CURRENCIES.USD
                )
                totalAmount += convertedAmount
            } else {
                totalAmount += op["amount_in_account_currency_at_creation"]
            }
        })
        return totalAmount
    }


    const getTotalAmountOfOperations = async () => {
        try {
            const filteredOperations = filterOperationsByMonth(props.data.operations)
            const totalIncomeAmount = await getAmountOfOperations(filteredOperations.incomes, "incomes")
            const totalSpendingAmount = await getAmountOfOperations(filteredOperations.spendings, "spendings")
            return {incomes: totalIncomeAmount, spendings: totalSpendingAmount}
        } catch (e) {
            props.setErrorMsg(`${e}`)
        }
    }

    useEffect(() => {
        getTotalAmountOfOperations().then(d => {
            setTotalIncomeAmount(d.incomes);
            setTotalSpendingAmount(d.spendings)
        }).finally(() => setIsLoading(false))
    })

    const CustomTooltip = ({active, payload}) => {
        if (active && payload && payload.length) {
            return (
                <div className="custom-tooltip p-1 d-flex align-items-center justify-content-center"
                     style={{background: "rgba(255, 255, 255, 1)"}}
                >
                    <p className="label m-0 text-nowrap">{`${payload[0].name} : ${prettifyFloat(payload[0].value.toFixed(2))} $`}</p>
                </div>
            );
        }
        return null;
    };

    const renderCustomizedLabel = ({cx, cy, midAngle, innerRadius, outerRadius, percent}) => {
        if (percent >= 0.001) {
            const RADIAN = Math.PI / 180;
            const radius = innerRadius + (outerRadius - innerRadius) * 0.4;
            const x = cx + radius * Math.cos(-midAngle * RADIAN);
            const y = cy + radius * Math.sin(-midAngle * RADIAN);

            return (
                <text
                    x={x}
                    y={y}
                    fill="black"
                    fontSize="12"
                    textAnchor="middle"
                    dominantBaseline="central"
                >
                    {`${(percent * 100).toFixed(1)}%`}
                </text>
            );
        }
    };
    return (
        <MainPageCard
            navigateto={OPERATIONS_ROUTE}
            style={{minWidth: "340px"}}
        >
            {isLoading
                ?
                <div className="d-flex align-items-center justify-content-center w-100" style={{minHeight: "105px"}}>
                    <Spinner animation="border"/>
                </div>
                :
                <div className="d-flex flex-row align-items-center w-100 gap-3"
                >
                    <PieChart width={150} height={100} style={{cursor: "pointer"}}>
                        <Pie
                            animationBegin={200}
                            animationDuration={700}
                            dataKey="value"
                            data={totalIncomeAmount || totalSpendingAmount ? dataForPie : emptyDataForPie}
                            innerRadius={20}
                            outerRadius={50}
                            labelLine={false}
                            label={totalIncomeAmount || totalSpendingAmount ? renderCustomizedLabel : null}
                            fill="#8884d8"
                        >
                            {dataForPie.map((entry, index) => (
                                <Cell
                                    key={`cell-${index}`}
                                    style={{outline: "none"}}
                                    fill={totalIncomeAmount || totalSpendingAmount ? entry["color"] : "#e1e0e0"}
                                />
                            ))}
                        </Pie>
                        {totalIncomeAmount || totalSpendingAmount ?
                            <Tooltip content={<CustomTooltip/>}
                                     wrapperStyle={{outline: "1px solid black", borderRadius: "3px"}}/> : null}
                    </PieChart>
                    <div className="d-flex w-100 flex-column">
                        <b className="text-nowrap">{props.month === "this-month" ? "This month" : "Previous month"}</b>
                        <div className="d-flex w-100 justify-content-between align-items-center">
                            <img
                                src={green_arrow}
                                alt=""
                                width={18}
                                height={18}
                            />
                            <p className="m-0 text-nowrap"
                               style={{color: INTERFACE_COLORS.GREEN}}>{prettifyFloat(totalIncomeAmount.toFixed(2))} $
                            </p>
                        </div>
                        <div className="d-flex w-100 justify-content-between align-items-center">
                            <img
                                src={red_arrow}
                                alt=""
                                width={18}
                                height={18}
                            />
                            <p className="m-0 text-nowrap"
                               style={{color: INTERFACE_COLORS.RED}}>-{prettifyFloat(totalSpendingAmount.toFixed(2))} $
                            </p>
                        </div>
                        <div className="m-0 d-flex w-100 justify-content-end align-items-center">
                            <div className="w-50 my-1" style={{height: "1px", background: "#e1e0e0"}}></div>
                        </div>
                        <div
                            className="d-flex w-100 justify-content-end align-items-center"
                        >
                            <p
                                className="text-nowrap m-0"
                                style={
                                    {
                                        color: totalIncomeAmount > totalSpendingAmount ? INTERFACE_COLORS.GREEN :
                                            totalIncomeAmount < totalSpendingAmount ? INTERFACE_COLORS.RED : null
                                    }
                                }
                            >
                                {prettifyFloat((totalIncomeAmount - totalSpendingAmount).toFixed(2))} $
                            </p>
                        </div>
                    </div>
                </div>}
        </MainPageCard>
    );
};

export default MonthTransactionsCard;