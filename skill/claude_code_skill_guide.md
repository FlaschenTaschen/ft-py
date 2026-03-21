# Creating a Skill for Claude Code

## Overview

A **skill** in Claude Code is a reusable capability that allows the
model to perform specific tasks more effectively. Skills typically
include instructions, context, and examples.

------------------------------------------------------------------------

## 1. Define the Purpose

Start by clearly identifying what your skill should do.

**Examples:** - Code refactoring - API integration - Data transformation

------------------------------------------------------------------------

## 2. Structure of a Skill

A typical skill includes:

### a. Name

A short, descriptive title.

### b. Description

Explain what the skill does and when to use it.

### c. Instructions

Step-by-step guidance for the model.

### d. Examples

Provide input/output examples to guide behavior.

------------------------------------------------------------------------

## 3. Example Skill

``` markdown
Name: JSON Formatter

Description:
Formats raw JSON into clean, readable structure.

Instructions:
1. Parse the input JSON
2. Validate syntax
3. Output formatted JSON with indentation

Examples:
Input:
{"name":"John","age":30}

Output:
{
  "name": "John",
  "age": 30
}
```

------------------------------------------------------------------------

## 4. Best Practices

-   Keep instructions clear and concise
-   Include multiple examples
-   Avoid ambiguity
-   Test iteratively

------------------------------------------------------------------------

## 5. Testing Your Skill

-   Run sample inputs
-   Validate outputs
-   Refine instructions as needed

------------------------------------------------------------------------

## 6. Deployment

Once finalized: - Integrate into Claude Code environment - Call the
skill via prompts or workflows

------------------------------------------------------------------------

## Conclusion

Creating effective skills improves reliability and consistency when
working with Claude Code.
