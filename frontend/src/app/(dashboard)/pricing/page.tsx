'use client';

import React from 'react';
import { ProtectedRoute, useUser } from '../../components/ProtectedRoute';

function PricingPageContent() {
  const user = useUser();

  return (
    <div className="min-h-full">
      <div className="mx-auto max-w-7xl px-4 py-6 my-10 sm:px-6 lg:px-8">
        <h1 className="text-4xl font-bold text-center">Manage your plan</h1>
        <div className="mt-10">
          <stripe-pricing-table 
            pricing-table-id={`${process.env.NEXT_PUBLIC_STRIPE_PRICING_TABLE_ID}`}
            publishable-key={`${process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY}`}
            client-reference-id={user?.pk ?? ''}
            customer-email={user?.email ?? ''}
          />
        </div>
      </div>
    </div>
  );
}

export default function PricingPage() {
  return (
    <ProtectedRoute>
      <PricingPageContent />
    </ProtectedRoute>
  );
}

// TypeScript declaration for the custom element
declare global {
  // eslint-disable-next-line @typescript-eslint/no-namespace
  namespace JSX {
    interface IntrinsicElements {
      'stripe-pricing-table': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement>, HTMLElement>;
    }
  }
}
