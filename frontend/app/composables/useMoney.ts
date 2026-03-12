import { useCurrencyStore } from "~/stores/currency"

export function useMoney() {

  const currency = useCurrencyStore()

  const formatter = computed(() => {
    return new Intl.NumberFormat(currency.locale, {
      style: "currency",
      currency: currency.code
    })
  })

  function format(amount: number | string) {
    return formatter.value.format(Number(amount))
  }

  return {
    format
  }

}