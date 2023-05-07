export const handleAmountOnChange = (value, setEnteredAmount, setEnteredAmountError) => {
    if (Number.isNaN(+value)) {
        return
    }
    if (value.toString().includes('.') && value.split('.')[1].length > 2) {
        return
    }
    if (value && value <= 0) {
        setEnteredAmountError("Amount must be greater than 0")
        return
    }
    if (value >= 1000000000) {
        setEnteredAmountError("Amount is too long")
        return
    }
    setEnteredAmount(value)
    setEnteredAmountError("")
}

