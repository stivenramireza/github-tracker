resource "aws_iam_policy" "can_get_db_password" {
  name        = "can-get-db-password"
  path        = "/"
  description = "Allow access to retrieve secrets from Secrets Manager"

  policy = jsonencode({
    Version : "2012-10-17",
    Statement : [
      {
        Effect : "Allow",
        Action : [
          "secretsmanager:GetSecretValue"
        ],
        Resource : [
          "arn:aws:secretsmanager:us-east-2:328697830963:secret:rds!db-4a17b183-e653-4743-a595-288d88b7e0d3-zfftiH"
        ]
      }
    ]
  })
}

output "can_get_db_password_arn" {
  value = aws_iam_policy.can_get_db_password.arn
}
