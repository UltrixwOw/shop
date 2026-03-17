// types/pinia.d.ts
import type { Pinia } from 'pinia'

declare module '#app' {
  interface NuxtApp {
    $pinia: Pinia
  }
}