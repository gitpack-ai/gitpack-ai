'use client';

import React from 'react';
import { ProtectedRoute } from '../../components/ProtectedRoute';

export default function PricingPage() {
  return (
    <ProtectedRoute>
        <div className="min-h-full">
            <div className="mx-auto max-w-7xl px-4 py-6 my-10 sm:px-6 lg:px-8">
                <h1 className="text-4xl font-bold text-center">Manage your plan</h1>
                <div className="mt-10">
                    <stripe-pricing-table 
                        pricing-table-id={`${process.env.NEXT_PUBLIC_STRIPE_PRICING_TABLE_ID}`}
                        publishable-key={`${process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY}`}
                    />
                </div>
            </div>
        </div>
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
