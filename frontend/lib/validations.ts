import { z } from "zod";

export const searchSchema = z.object({
  query: z
    .string()
    .min(10, "Please describe what you're looking for (at least 10 characters)")
    .max(200, "Keep it under 200 characters"),
});

export type SearchFormData = z.infer<typeof searchSchema>;
