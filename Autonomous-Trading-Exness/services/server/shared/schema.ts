import { pgTable, text, serial, integer, boolean, timestamp, jsonb } from "drizzle-orm/pg-core";
import { createInsertSchema, createSelectSchema } from "drizzle-zod";
import { z } from "zod";

export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  username: text("username").notNull().unique(),
  password: text("password").notNull(),
  email: text("email").unique(),
  role: text("role").default("user").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const tradingAccounts = pgTable("trading_accounts", {
  id: serial("id").primaryKey(),
  accountName: text("account_name").notNull(),
  broker: text("broker").notNull(),
  accountId: text("account_id").notNull(),
  platform: text("platform").notNull(),
  balance: text("balance"),
  currency: text("currency").default("USD"),
  isActive: boolean("is_active").default(true).notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const positions = pgTable("positions", {
  id: serial("id").primaryKey(),
  accountId: integer("account_id").references(() => tradingAccounts.id),
  symbol: text("symbol").notNull(),
  type: text("type").notNull(), // BUY or SELL
  size: text("size").notNull(),
  entryPrice: text("entry_price").notNull(),
  status: text("status").default("open").notNull(), // open or closed
  openTime: timestamp("open_time").defaultNow().notNull(),
  closeTime: timestamp("close_time"),
  profit: text("profit"),
});

export const notifications = pgTable("notifications", {
  id: serial("id").primaryKey(),
  title: text("title").notNull(),
  message: text("message").notNull(),
  type: text("type").notNull(), // info, success, warning, error
  isRead: boolean("is_read").default(false).notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const educationalResources = pgTable("educational_resources", {
  id: serial("id").primaryKey(),
  title: text("title").notNull(),
  description: text("description").notNull(),
  skillLevel: text("skill_level").notNull(), // beginner, intermediate, advanced
  category: text("category").notNull(), // programming, design, marketing, data-science
  resourceType: text("resource_type").notNull(), // video, article, course, tutorial
  duration: text("duration"),
  imageUrl: text("image_url"),
  featured: boolean("featured").default(false).notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const botConfig = pgTable("bot_config", {
  id: serial("id").primaryKey(),
  symbols: jsonb("symbols").notNull(),
  marketOpen: text("market_open").notNull(),
  marketClose: text("market_close").notNull(),
  intervalMinutes: integer("interval_minutes").notNull(),
  isEnabled: boolean("is_enabled").default(true).notNull(),
  apiProvider: text("api_provider").default("gemini").notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
});

// Zod schemas
export const insertUserSchema = createInsertSchema(users);
export const selectUserSchema = createSelectSchema(users);
export const botConfigInsertSchema = createInsertSchema(botConfig);
export const botConfigSelectSchema = createSelectSchema(botConfig);

export type User = z.infer<typeof selectUserSchema>;
export type InsertUser = z.infer<typeof insertUserSchema>;
export type TradingAccount = z.infer<typeof createSelectSchema(tradingAccounts)>;
export type Position = z.infer<typeof createSelectSchema(positions)>;
export type Notification = z.infer<typeof createSelectSchema(notifications)>;
export type EducationalResource = z.infer<typeof createSelectSchema(educationalResources)>;
export type BotConfig = z.infer<typeof botConfigSelectSchema>;
