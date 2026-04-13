<script setup lang="ts">
import type { ButtonProps } from "@nuxt/ui";

const localePath = useLocalePath();

const { t } = useI18n();

const links = ref<ButtonProps[]>([
  {
    label: t('start_shopping'),
    to: localePath('/products'),
    icon: "i-heroicons-shopping-bag",
  },
  {
    label: t('learn_more'),
    to: localePath('/about'),
    color: "neutral",
    variant: "subtle",
    trailingIcon: "i-lucide-arrow-right",
  },
]);

const cards = ref([
  {
    title: t('fast_delivery'),
    description: t('fast_delivery_desc'),
    icon: "i-heroicons-truck",
  },
  {
    title: t('secure_payment'),
    description: t('secure_payment_desc'),
    icon: "i-heroicons-shield-check",
  },
  {
    title: t('support_247'),
    description: t('support_247_desc'),
    icon: "i-heroicons-chat-bubble-left-right",
  },
]);
</script>

<template>
  <UContainer>
    <div>
      <UPageHero
        :title="$t('meloni_greeting')"
        :description="$t('discover_products')"
        :links="links"
      />
    </div>
    <div>
      <UPageGrid>
        <UPageCard v-for="(card, index) in cards" :key="index" v-bind="card" />
      </UPageGrid>
    </div>
  </UContainer>
</template>
