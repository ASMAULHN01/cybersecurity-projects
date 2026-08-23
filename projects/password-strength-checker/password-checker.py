import re

def check_password_strength(password):
    strength = 0
    feedback = []
    
    if len(password) >= 8:
        strength += 1
    else:
        feedback.append("At least 8 characters")
    
    if re.search(r'[a-z]', password):
        strength += 1
    else:
        feedback.append("Add lowercase letters")
    
    if re.search(r'[A-Z]', password):
        strength += 1
    else:
        feedback.append("Add uppercase letters")
    
    if re.search(r'[0-9]', password):
        strength += 1
    else:
        feedback.append("Add numbers")
    
    if re.search(r'[!@#$%^&*]', password):
        strength += 1
    else:
        feedback.append("Add special characters")
    
    return strength, feedback

if __name__ == "__main__":
    password = "Test@1234"
    strength, feedback = check_password_strength(password)
    
    print(f"Password: {password}")
    print(f"Strength: {strength}/5")
    if feedback:
        print(f"Suggestions: {', '.join(feedback)}")
    else:
        print("Strong password!")
