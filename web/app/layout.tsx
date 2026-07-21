import type { Metadata } from "next";

import "./globals.css";

export const metadata: Metadata = {
  title: "Learn English from someone who already talks the way you do.",
  description:
    "Most apps help you sound like a native speaker. We find the native speaker who already sounds like you."
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <head>
        <link
          href="https://api.fontshare.com/v2/css?f[]=clash-display@500,600&display=swap"
          rel="stylesheet"
        />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="font-body">{children}</body>
    </html>
  );
}
