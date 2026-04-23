<template>
  <UContainer>
    <div class="footer-container">
    <div class="footer-box">
      <div class="flex justify-between">
        <UColorModeButton variant="ghost" size="sm" />
        <div>
          <AppLanguageSwitcher />
        </div>
      </div>
    </div>
    <div class="footer-box">
      <div>
        <p>
          {{ $t("wake_server") }}
          <a class="backend-link" href="https://meloni-backend.onrender.com/" target="_blank"
            >https://meloni-backend.onrender.com/</a
          >
        </p>
      </div>
    </div>
    </div>
  </UContainer>
</template>

<style lang="scss">
.footer-container {
  margin: 20px 0;
}
.footer-box {
  margin: 20px 0;
}
.backend-link {
  text-decoration: underline;
}
</style>
