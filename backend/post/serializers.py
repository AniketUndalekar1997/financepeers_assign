from rest_framework import serializers
from .models import User
from .models import Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'userId', 'title', 'body')


class FileDataSerializer(serializers.Serializer):
    """
    "userId": 1,
    "id": 1,
    "title"
    "body"
    """
    userId = serializers.IntegerField(required=True)
    id = serializers.IntegerField(required=True)
    title = serializers.CharField(required=True, max_length=200)
    body = serializers.CharField(required=True, max_length=10000)

    def create(self, data):
        print("serializer", data)
        is_post = Post.objects.create(**data)
        is_post.save()
        return is_post
        # is_post = None
        # try:
        #     print(f"******* data:{data}")
        #     is_post = Post.objects.filter(id=data.get("id"))
        # except:
        #     print(traceback.format_exc())
        # print(f"is_post: {is_post}")
        # if is_post:
        #     # Update here
        #     print("Should update now")
        #     us_updated = is_post.update(title=data.get("title"))
        #     print(f"us_updated:{us_updated}")
        # else:
        #     is_post = Post.objects.create(**data)
        #     is_post.save()
        # return is_post
