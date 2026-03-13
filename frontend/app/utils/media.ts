export const media = (path?: string) => {
  if (!path) return '/images/productPreview.png'

  if (path.startsWith('http')) return path

  return `http://127.0.0.1:8000${path}`
}