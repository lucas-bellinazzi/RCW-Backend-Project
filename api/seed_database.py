"""
Script to seed the database with mock data for testing purposes.
This script imports and executes the main seeder from the seed package.
"""

import sys
from app import create_app
from seed.seeder import run_seeder


def main():
    """Main function to run the seeding script."""
    print("="*60)
    print("DATABASE SEEDING SCRIPT")
    print("="*60)
    
    # Create Flask app context
    app = create_app()
    
    with app.app_context():
        try:
            # Run the seeder
            run_seeder()
            
            print("✓ Database seeding completed successfully!")
            return 0
            
        except Exception as e:
            print(f"\n✗ Error during seeding: {str(e)}")
            import traceback
            traceback.print_exc()
            return 1


if __name__ == '__main__':
    sys.exit(main())
