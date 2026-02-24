<template>
  <div class="admin-layout">
    <aside class="sidebar">
      <NuxtLink to="/admin/products">Products</NuxtLink>
      <NuxtLink to="/admin/orders">Orders</NuxtLink>
    </aside>

    <main class="admin-content">
      <slot />
    </main>
  </div>
</template>

<style scoped>
.admin-layout {
  display: flex;
}
.sidebar {
  width: 220px;
  background: #111;
  color: white;
  padding: 20px;
}
.admin-content {
  flex: 1;
  padding: 20px;
}
</style>