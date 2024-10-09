import Script from 'next/script'

export default function PricingLayout({ children }: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <>
      <Script
        async
        src="https://js.stripe.com/v3/pricing-table.js"
        strategy="afterInteractive"
      />
      {children}
    </>
  )
}