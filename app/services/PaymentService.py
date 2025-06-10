
class PaymentService:
    @staticmethod
    def create_payment_submission(
        db: Session,
        user_id: str,
        payment_data: PaymentSubmissionCreate
    ) -> PaymentSubmission:
        submission = PaymentSubmission(
            user_id=user_id,
            plan_id=payment_data.plan_id,
            screenshot_url=payment_data.screenshot_url
        )
        db.add(submission)
        db.commit()
        db.refresh(submission)
        return submission

    @staticmethod
    def verify_payment(
        db: Session,
        submission_id: str,
        status: PaymentStatus,
        verified_by: str
    ) -> PaymentSubmission:
        submission = db.get(PaymentSubmission, submission_id)
        if not submission:
            raise ValueError("Payment submission not found")
        
        submission.status = status
        submission.verified_by = verified_by
        
        if status == PaymentStatus.VERIFIED:
            SubscriptionService.subscribe_user(
                db=db,
                user_id=submission.user_id,
                plan_id=submission.plan_id
            )
        
        db.commit()
        db.refresh(submission)
        return submission

    @staticmethod
    def get_user_submissions(
        db: Session,
        user_id: str
    ) -> list[PaymentSubmission]:
        return db.execute(
            select(PaymentSubmission)
            .filter_by(user_id=user_id)
            .order_by(PaymentSubmission.created_at.desc())
        ).scalars().all()