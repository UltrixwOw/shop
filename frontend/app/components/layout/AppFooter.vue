<template>
  <UContainer>
    <div class="flex justify-between">
      <UColorModeButton variant="ghost" size="sm" />
      <div>
        <AppLanguageSwitcher />
      </div>
    </div>
    <div>
      <p> 
      {{ $t("dev_warning") }}
      </p>
      <p>
      {{ $t("wake_server") }}
      <a href="https://meloni-backend.onrender.com/">https://meloni-backend.onrender.com/</a>
      </p>
    </div>
  </UContainer>
</template>
