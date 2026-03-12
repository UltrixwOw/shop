import { defineStore } from 'pinia'

export const useCurrencyStore = defineStore('currency', () => {

  const code = ref("EUR")
  const symbol = ref("€")
  const locale = ref("de-DE")

  function setCurrency(newCode: string, newSymbol: string, newLocale: string) {
    code.value = newCode
    symbol.value = newSymbol
    locale.value = newLocale
  }

  return {
    code,
    symbol,
    locale,
    setCurrency
  }

})