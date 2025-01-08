from flask import request, jsonify
from app import db
from models import User, Expense, Income, Budget, RecurringExpense
from datetime import datetime

def init_routes(app):
    # Set Budget Limit
    @app.route('/budget', methods=['POST'])
    def set_budget():
        data = request.get_json()
        if not data.get('category') or not data.get('limit'):
            return jsonify({'message': 'Missing required fields'}), 400

        new_budget = Budget(category=data['category'], limit=data['limit'], user_id=1)  # Assume user_id=1 for simplicity
        db.session.add(new_budget)
        db.session.commit()
        return jsonify({'message': 'Budget set successfully'}), 201

    # Get All Budgets
    @app.route('/budgets', methods=['GET'])
    def get_budgets():
        budgets = Budget.query.filter_by(user_id=1).all()  # Assume user_id=1
        return jsonify([{
            'category': budget.category,
            'limit': budget.limit,
            'date_set': budget.date_set
        } for budget in budgets]), 200

    # Compare Budget vs Actual Expenses
    @app.route('/budget/compare', methods=['GET'])
    def compare_budget_expenses():
        budgets = Budget.query.filter_by(user_id=1).all()  # Assume user_id=1
        budget_comparison = []
        
        for budget in budgets:
            actual_expenses = db.session.query(db.func.sum(Expense.amount)).filter_by(category=budget.category).scalar() or 0
            budget_comparison.append({
                'category': budget.category,
                'budget_limit': budget.limit,
                'actual_expenses': actual_expenses,
                'difference': budget.limit - actual_expenses
            })
        
        return jsonify(budget_comparison), 200

    # Add Expense
    @app.route('/expense', methods=['POST'])
    def add_expense():
        data = request.get_json()
        new_expense = Expense(
            description=data['description'],
            amount=data['amount'],
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            category=data['category'],
            tags=data.get('tags'),
            user_id=1  # Assume user_id=1 for simplicity
        )
        db.session.add(new_expense)
        db.session.commit()
        return jsonify({'message': 'Expense added successfully'}), 201

    # Get Expenses
    @app.route('/expenses', methods=['GET'])
    def get_expenses():
        expenses = Expense.query.filter_by(user_id=1).all()  # Assume user_id=1
        return jsonify([{
            'id': expense.id,
            'description': expense.description,
            'amount': expense.amount,
            'date': expense.date,
            'category': expense.category,
            'tags': expense.tags
        } for expense in expenses]), 200

    # Dashboard Overview
    @app.route('/dashboard', methods=['GET'])
    def dashboard():
        total_expenses = db.session.query(db.func.sum(Expense.amount)).filter_by(user_id=1).scalar() or 0
        total_income = db.session.query(db.func.sum(Income.amount)).filter_by(user_id=1).scalar() or 0
        savings = total_income - total_expenses
        return jsonify({
            'total_expenses': total_expenses,
            'total_income': total_income,
            'savings': savings
        }), 200



